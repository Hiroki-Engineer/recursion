import math
from enum import StrEnum, auto
from typing import Any, Literal

from pydantic import BaseModel, field_validator


class Method(StrEnum):
    Floor = auto()
    Nroot = auto()
    Reverse = auto()
    ValidAnagram = auto()
    Sort = auto()


class Result(BaseModel):
    results: str
    result_type: str
    id: int | None = None


class FloorFunctionModel(BaseModel):
    method: Literal[Method.Floor]
    params: list[float]

    @field_validator("params")
    @classmethod
    def validate_params(cls, value: list[float]) -> list[float]:
        if len(value) != 1:
            raise ValueError
        return value

    def result(self) -> Result:
        return Result(
            results=str(math.floor(self.params[0])),
            result_type="int",
        )


class NrootFunctionModel(BaseModel):
    method: Literal[Method.Nroot]
    params: list[int]

    @field_validator("params")
    @classmethod
    def validate_params(cls, value: list[int]) -> list[int]:
        if len(value) != 2:  # noqa: PLR2004 (simply want to use 2 params)
            raise ValueError
        return value

    def result(self) -> Result:
        return Result(
            results=str(self.params[0] ** self.params[1]),
            result_type="int",
        )


class ReverseFunctionmodel(BaseModel):
    method: Literal[Method.Reverse]
    params: list[str]

    @field_validator("params")
    @classmethod
    def validate_params(cls, value: list[str]) -> list[str]:
        if len(value) != 1:
            raise ValueError
        return value

    def result(self) -> Result:
        return Result(
            results=str(self.params[0][::-1]),
            result_type="str",
        )


class ValidAnagramFunctionModel(BaseModel):
    method: Literal[Method.ValidAnagram]
    params: list[str]

    @field_validator("params")
    @classmethod
    def validate_params(cls, value: list[str]) -> list[str]:
        if len(value) != 2:  # noqa: PLR2004 (simply want to use 2 params)
            raise ValueError
        return value

    def result(self) -> Result:
        return Result(
            results=str(sorted(self.params[0]) == sorted(self.params[1])),
            result_type="bool",
        )


class SortFunctionModel(BaseModel):
    method: Literal[Method.Sort]
    params: list[str]

    def result(self) -> Result:
        return Result(
            results=str(sorted(self.params)),
            result_type="list",
        )


class RequestBaseModel(BaseModel):
    method: Method
    params: Any
    param_types: list[str]  # implementation skipped
    id: int  # implementation skipped

    def parse_function_model(
        self,
    ) -> FloorFunctionModel | NrootFunctionModel | ReverseFunctionmodel | ValidAnagramFunctionModel | SortFunctionModel:
        if self.method == Method.Floor:
            return FloorFunctionModel(method=self.method, params=self.params)

        if self.method == Method.Nroot:
            return NrootFunctionModel(
                method=self.method,
                params=self.params,
            )

        if self.method == Method.Reverse:
            return ReverseFunctionmodel(
                method=self.method,
                params=self.params,
            )

        if self.method == Method.ValidAnagram:
            return ValidAnagramFunctionModel(
                method=self.method,
                params=self.params,
            )

        if self.method == Method.Sort:
            return SortFunctionModel(
                method=self.method,
                params=self.params,
            )

        raise ValueError
