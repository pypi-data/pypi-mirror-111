from dataclasses import dataclass
from typing import Union

import pendulum
from pyspark.sql import Column
from pyspark.sql.functions import expr
from pyspark.sql.functions import lit
from typeguard import typechecked

from tecton_spark.errors import TectonValidationError


@dataclass
class BaseMaterializationContext:
    _feature_start_time: pendulum.DateTime
    _feature_end_time: pendulum.DateTime

    @property
    def feature_start_time(self) -> pendulum.DateTime:
        return self._feature_start_time

    @property
    def feature_end_time(self) -> pendulum.DateTime:
        return self._feature_end_time

    @property
    def feature_start_time_string(self) -> str:
        return self.feature_start_time.to_datetime_string()

    @property
    def feature_end_time_string(self) -> str:
        return self.feature_end_time.to_datetime_string()

    @typechecked
    def feature_time_filter_sql(self, timestamp_expr: str) -> str:
        return f"('{self.feature_start_time_string}' <= ({timestamp_expr}) AND ({timestamp_expr}) < '{self.feature_end_time_string}')"

    @typechecked
    def feature_time_filter_pyspark(self, timestamp_expr: Union[str, Column]) -> Column:
        if isinstance(timestamp_expr, str):
            timestamp_expr = expr(timestamp_expr)
        return (lit(self.feature_start_time_string) <= timestamp_expr) & (
            timestamp_expr < lit(self.feature_end_time_string)
        )

    # TODO: better name
    def tile_ends(self, slide_interval):
        if self.feature_start_time == self.feature_end_time:
            return "ARRAY()"
        else:
            try:
                amount, unit = slide_interval.split()
                amount = int(amount)
            except ValueError:
                raise ValueError("Slide interval must follow format '{AMOUNT} {UNIT}'")

            allowed_units = ["day", "days", "hour", "hours", "minute", "minutes"]
            if unit.lower() not in ["day", "days", "hour", "hours", "minute", "minutes"]:
                raise ValueError(f"Allowed units are {allowed_units}")

            if amount <= 0:
                raise ValueError(f"Slide interval {slide_interval} must be positive")
            return (
                "ARRAY("
                + ", ".join(
                    [
                        f"TO_TIMESTAMP('{x.to_datetime_string()}')"
                        for x in (self.feature_end_time - self.feature_start_time).range(unit=unit, amount=amount)
                    ][1:]
                )
                + ")"
            )


@dataclass
class UnboundMaterializationContext(BaseMaterializationContext):
    """
    This is only meant for instantiation in transformation default args. Using it directly will fail.
    """

    @property
    def feature_start_time(self):
        raise TectonValidationError(
            "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        )

    @property
    def feature_end_time(self):
        raise TectonValidationError(
            "tecton.materialization_context() must be passed in via a kwarg default only. Instantiation in function body is not allowed."
        )


@dataclass
class BoundMaterializationContext(BaseMaterializationContext):
    pass


def materialization_context():
    dummy_time = pendulum.datetime(1970, 1, 1)
    return UnboundMaterializationContext(_feature_start_time=dummy_time, _feature_end_time=dummy_time)
