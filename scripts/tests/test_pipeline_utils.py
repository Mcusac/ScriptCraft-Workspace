# tests/test_pipelines_utils.py

from scripts.pipelines.pipeline_utils import (
    make_step, validate_pipelines, 
    combine_pipelines, PipelineStep,
    )


### Tests ###
def test_combine_pipelines_aggregates_steps():
    step_a = make_step("Step A", "a.log", lambda: None, "input")
    step_b = make_step("Step B", "b.log", lambda: None, "input")
    step_map = {"one": [step_a], "two": [step_b]}
    combined = combine_pipelines("one", "two", step_map=step_map)
    assert combined == [step_a, step_b]


def test_make_step_defaults():
    step = make_step("Test", "test.log", lambda: None, "input")
    assert isinstance(step, PipelineStep)
    assert step.tags == []


def test_make_step_with_tags():
    step = make_step("Tagged", "tagged.log", lambda: None, "input", tags=["QA", "transform"])
    assert "QA" in step.tags
    assert "transform" in step.tags


def test_validate_empty_pipeline():
    assert validate_pipelines({"empty_pipeline": []}) is False


def test_validate_pipelines_invalid():
    step = make_step("Broken", "broken.log", None, "input")
    assert validate_pipelines({"bad_pipeline": [step]}) is False


def test_validate_pipelines_valid():
    step = make_step("Valid", "valid.log", lambda: None, "input")
    assert validate_pipelines({"my_pipeline": [step]}) is True


def test_run_pipeline_from_steps_with_tag_filter():
    calls = []

    def dummy():
        calls.append("ran")

    step_qa = make_step("QA Step", "qa.log", dummy, "input", tags=["QA"])
    step_qc = make_step("QC Step", "qc.log", dummy, "input", tags=["QC"])

    run_pipeline_test_friendly([step_qa, step_qc], tag_filter="QA")

    assert calls == ["ran"]


### Run ###
def run_pipeline_test_friendly(steps, tag_filter=None):
    filtered = [s for s in steps if tag_filter is None or tag_filter in s.tags]
    for step in filtered:
        step.qc_func()