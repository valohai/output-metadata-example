"""Miscellaneous helper functions."""

import datetime
from typing import Generator

from faker import Faker  # type: ignore

# initialize the dummy data generator on module load
fake = Faker()


def iso_date() -> str:
    """Return the current date in ISO format."""
    return datetime.date.today().isoformat()


def random_filenames(nr_files: int) -> Generator[str, None, None]:
    """Generate random, unique filenames."""
    return (fake.unique.file_name(extension="txt") for _ in range(nr_files))


def random_paragraphs() -> str:
    """Generate a random number of paragraphs."""
    return "\n".join(fake.paragraphs())


def dummy_metadata():
    """Generate dummy key-value pairs.

    Restrict types to JSON-serializable ones.
    """
    return fake.pydict(
        value_types=[str, int, float, bool],
        nb_elements=fake.pyint(min_value=1, max_value=10),
    )