from assistant.explain import explain

result = {
    "total_units": 345,
    "estimated_cost": 2760
}

answer = explain(
    "Why was my electricity bill high?",
    result
)

print(answer)