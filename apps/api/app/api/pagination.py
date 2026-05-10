from app.schemas.pagination import PaginationMeta


def build_pagination_meta(total: int, limit: int, offset: int, returned_count: int) -> PaginationMeta:
    return PaginationMeta(
        total=total,
        limit=limit,
        offset=offset,
        has_more=(offset + returned_count) < total,
    )
