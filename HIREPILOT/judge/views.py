from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Problem, Submission, TestCase
from .forms import SubmissionForm
import json
from .runner import run_python_code

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, "judge/problem_list.html", {"problems": problems})

def problem_detail(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    return render(request, "judge/problem_detail.html", {"problem": prob})

def submit_solution(request, slug):
    prob = get_object_or_404(Problem, slug=slug)
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            submission = Submission.objects.create(
                user=request.user if request.user.is_authenticated else None,
                problem=prob,
                code=code,
                status='RUNNING',
            )

            # Run against testcases synchronously (demo). Hide hidden TCs if desired.
            tcs = prob.testcases.all()
            results = []
            all_passed = True
            total_time = 0.0
            for tc in tcs:
                exit_code, stdout, stderr, t_taken = run_python_code(code, tc.input_data)
                total_time += t_taken
                passed = False
                verdict = ""
                if exit_code is None:
                    verdict = "TLE"
                    passed = False
                elif exit_code != 0:
                    verdict = f"RE: {stderr.strip()[:300]}"
                    passed = False
                else:
                    # Normalize whitespace to compare
                    out_clean = stdout.strip()
                    expected_clean = tc.expected_output.strip()
                    if out_clean == expected_clean:
                        verdict = "AC"
                        passed = True
                    else:
                        verdict = f"WA - expected {expected_clean!r} but got {out_clean!r}"
                        passed = False

                results.append({
                    "tc_id": tc.id,
                    "passed": passed,
                    "verdict": verdict,
                    "stdout": stdout,
                    "stderr": stderr,
                    "time": t_taken
                })
                if not passed:
                    all_passed = False

            submission.runtime = total_time
            submission.details = json.dumps(results, indent=2)
            submission.status = 'AC' if all_passed else 'WA'
            submission.save()

            return redirect('judge:submission_result', submission_id=submission.id)
    else:
        form = SubmissionForm()
    return render(request, "judge/submit.html", {"problem": prob, "form": form})

def submission_result(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)
    details = []
    try:
        details = json.loads(sub.details)
    except Exception:
        details = [{"error": "No details"}]
    return render(request, "judge/submission_result.html", {"submission": sub, "details": details})


@csrf_exempt
def run_code(request, slug):
    """AJAX endpoint — run code with custom user-provided stdin, return output as JSON."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        code = body.get("code", "")
        stdin = body.get("stdin", "")
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not code.strip():
        return JsonResponse({"stdout": "", "stderr": "No code provided.", "exit_code": -1, "time_taken": 0})

    exit_code, stdout, stderr, time_taken = run_python_code(code, stdin)

    return JsonResponse({
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "time_taken": round(time_taken, 3),
    })
