from typing import Any, Dict, Set, Union
from uuid import uuid4

from rich.style import Style
from vedro._core import Dispatcher, ScenarioResult
from vedro.events import ScenarioFailedEvent, ScenarioRunEvent, StepFailedEvent, StepPassedEvent
from vedro.plugins.director import RichReporter

__all__ = ("GitlabReporter",)


class GitlabReporter(RichReporter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._scenario_result: Union[ScenarioResult, None] = None
        self._scenario_steps: Dict[str, Set[str]] = {}
        self._prev_step_name: Union[str, None] = None
        self._prev_scope: Set[str] = set()

    def subscribe(self, dispatcher: Dispatcher) -> None:
        super().subscribe(dispatcher)
        dispatcher.listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end)

    def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        super().on_scenario_run(event)
        self._scenario_result = event.scenario_result
        self._scenario_steps = {}
        self._prev_step_name = None
        self._prev_scope = set()

    def on_step_end(self, event: StepPassedEvent) -> None:
        assert isinstance(self._scenario_result, ScenarioResult)

        step_name = event.step_result.step_name
        if self._scenario_result.scope:
            step_scope = set(self._scenario_result.scope.keys())
        else:
            step_scope = set()

        self._scenario_steps[step_name] = step_scope - self._prev_scope
        self._prev_scope = step_scope
        self._prev_step_name = step_name

    def on_scenario_failed(self, event: ScenarioFailedEvent) -> None:
        scenario_result = event.scenario_result

        if self._verbosity <= 2:
            self._print_scenario_subject(scenario_result)
            if self._verbosity == 1:
                self._print_collapsable_steps(scenario_result)
                self._print_exceptions(scenario_result)
            elif self._verbosity == 2:
                self._print_steps_with_collapsable_scope(scenario_result)
                self._print_exceptions(scenario_result)
        else:
            section_name = str(uuid4())
            started_at = int(scenario_result.started_at) if scenario_result.started_at else 0
            self._print_section_start(section_name, started_at, is_collapsed=False)
            self._print_scenario_subject(scenario_result)

            self._print_steps(scenario_result)
            self._print_exceptions(scenario_result)

            ended_at = int(scenario_result.ended_at) if scenario_result.ended_at else 0
            self._print_section_end(section_name, ended_at)

            self._print_collapsable_scope(scenario_result)

    def _print_section_start(self, name: str, started_at: int = 0,
                             is_collapsed: bool = True) -> None:
        collapsed = "true" if is_collapsed else "false"
        output = f'\033[0Ksection_start:{started_at}:{name}[collapsed={collapsed}]\r\033[0K'
        self._console.file.write(output)

    def _print_section_end(self, name: str, ended_at: int = 0) -> None:
        output = f'\033[0Ksection_end:{ended_at}:{name}\r\033[0K'
        self._console.file.write(output)

    def _print_steps(self, scenario_result: ScenarioResult) -> None:
        for step_result in scenario_result.step_results:
            self._print_step_name(step_result)

    def _print_exceptions(self, scenario_result: ScenarioResult) -> None:
        for step_result in scenario_result.step_results:
            if step_result.exc_info:
                self._print_exception(step_result.exc_info.value,
                                      step_result.exc_info.traceback)

    def _print_collapsable_steps(self, scenario_result: ScenarioResult) -> None:
        for step_result in scenario_result.step_results:
            section_name = str(uuid4())
            started_at = int(step_result.started_at) if step_result.started_at else 0
            self._print_section_start(section_name, started_at)

            self._print_step_name(step_result)

            scope = scenario_result.scope if scenario_result.scope else {}
            for key, val in self._format_scope(scope):
                if key in self._scenario_steps[step_result.step_name]:
                    self._console.out(f"      {key}: ", style=Style(color="blue"))
                    self._console.out(val)

            ended_at = int(step_result.ended_at) if step_result.ended_at else 0
            self._print_section_end(section_name, ended_at)

    def _print_steps_with_collapsable_scope(self, scenario_result: ScenarioResult) -> None:
        for step_result in scenario_result.step_results:
            self._print_step_name(step_result)

            scope = scenario_result.scope if scenario_result.scope else {}
            for key, val in self._format_scope(scope):
                if key in self._scenario_steps[step_result.step_name]:
                    section_name = str(uuid4())
                    self._print_section_start(section_name)
                    self._console.out(f"      {key}: ", style=Style(color="blue"))
                    self._console.out(val)
                    self._print_section_end(section_name)

    def _print_collapsable_scope(self, scenario_result: ScenarioResult) -> None:
        section_name = str(uuid4())
        self._print_section_start(section_name)
        self._print_scope(scenario_result.scope or {})
        self._print_section_end(section_name)
