from typing import TYPE_CHECKING, AnyStr, Dict, Optional

if TYPE_CHECKING:
    from ruleau.process import Process
    from ruleau.rule import Rule
    from ruleau.structures import RuleauDict


class ExecutionResult:
    def __init__(
        self,
        executed_rule: "Rule",
        payload: "RuleauDict",
        result,
        dependent_results: Dict[str, "ExecutionResult"],
        override: AnyStr = None,
        original_result: Optional[bool] = None,
        skipped: bool = False,
        failed: bool = False,
    ):
        self.executed_rule = executed_rule
        self.payload = payload
        self.result = result
        self.override = override
        self.original_result = original_result
        self.dependent_results = dependent_results
        self.skipped = skipped
        self.failed = failed

    @staticmethod
    def skipped_result(rule: "Rule"):
        return ExecutionResult(rule, None, None, {}, skipped=True)
