from typing import Generic, TypeVar, List
import strawberry
from strawberry.extensions import pyinstrument
import asyncio


T = TypeVar("T")


@strawberry.input(description="Filter for GraphQL queries")
class GraphQLFilter(Generic[T]):
    """EXTERNAL Filter for GraphQL queries"""

    eq: T | None = None
    in_: list[T] | None = None
    nin: list[T] | None = None
    gt: T | None = None
    gte: T | None = None
    lt: T | None = None
    lte: T | None = None
    contains: T | None = None
    icontains: T | None = None

@strawberry.input(description="Filter for GraphQL queries")
class GraphQLFilterStr(str):
    """EXTERNAL Filter for GraphQL queries"""

    eq: str | None = None
    in_: list[str] | None = None
    nin: list[str] | None = None
    gt: str | None = None
    gte: str | None = None
    lt: str | None = None
    lte: str | None = None
    contains: str | None = None
    icontains: str | None = None


@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    title: str

    @strawberry.field
    async def authors(
        self,
        # Test swapping the below lines to see the difference
        name: GraphQLFilter[str] | None = None,
        # name: GraphQLFilterStr | None = None,
    ) -> list[Author]:
        await asyncio.sleep(0.5)
        return [Author(name="F. Scott Fitzgerald")]


def get_books():
    return [
        Book(title="The Great Gatsby"),
    ] * 10000


@strawberry.type
class Query:
    books: List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(
    query=Query, extensions=[pyinstrument.PyInstrument(report_path="pyinstrument.html")]
)
