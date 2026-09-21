import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.repositories import movies_repository
from app.schemas.movies import MovieUpdateModel
from app.services import movies_services, user_services


class RegistrationServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_register_user_awaits_lookup_and_create(self):
        db = object()
        created_user = SimpleNamespace(id=1, email="person@example.com")

        with (
            patch.object(
                user_services.user_repository,
                "get_user_by_email",
                new=AsyncMock(return_value=None),
            ) as get_user_by_email,
            patch.object(
                user_services.user_repository,
                "create_user",
                new=AsyncMock(return_value=created_user),
            ) as create_user,
            patch.object(user_services, "hash_password", return_value="hashed") as hash_password,
        ):
            result = await user_services.register_user(db, "person@example.com", "password")

        self.assertIs(result, created_user)
        get_user_by_email.assert_awaited_once_with(db, "person@example.com")
        hash_password.assert_called_once_with("password")
        create_user.assert_awaited_once_with(db, "person@example.com", "hashed")


class MovieOwnershipServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_update_uses_movie_and_authenticated_owner_ids(self):
        db = object()
        movie = SimpleNamespace(id=10, owner_id=7)
        payload = MovieUpdateModel(title="Arrival")

        with (
            patch.object(
                movies_services.movies_repository,
                "get_by_id",
                new=AsyncMock(return_value=movie),
            ) as get_by_id,
            patch.object(
                movies_services.movies_repository,
                "update_movie",
                new=AsyncMock(return_value=movie),
            ) as update_movie,
        ):
            result = await movies_services.update_movies(db, 10, payload, 7)

        self.assertIs(result, movie)
        get_by_id.assert_awaited_once_with(db, 10, 7)
        update_movie.assert_awaited_once_with(db, payload, movie)

    async def test_update_returns_none_when_movie_is_not_owned_by_user(self):
        with patch.object(
            movies_services.movies_repository,
            "get_by_id",
            new=AsyncMock(return_value=None),
        ) as get_by_id:
            result = await movies_services.update_movies(
                object(), 10, MovieUpdateModel(year=2020), 7
            )

        self.assertIsNone(result)
        get_by_id.assert_awaited_once()


class MovieRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_delete_only_deletes_a_movie_returned_by_owner_scoped_query(self):
        movie = SimpleNamespace(id=10, owner_id=7)
        result = SimpleNamespace(scalars=lambda: SimpleNamespace(first=lambda: movie))
        db = SimpleNamespace(
            execute=AsyncMock(return_value=result),
            delete=AsyncMock(),
            commit=AsyncMock(),
        )

        deleted = await movies_repository.delete_movie(db, 10, 7)

        self.assertIs(deleted, movie)
        db.delete.assert_awaited_once_with(movie)
        db.commit.assert_awaited_once()

        query = db.execute.await_args.args[0]
        sql = str(query.compile(compile_kwargs={"literal_binds": True}))
        self.assertIn("movies.id = 10", sql)
        self.assertIn("movies.owner_id = 7", sql)
