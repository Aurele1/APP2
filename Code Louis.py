avions_diplomatic_50 = [
    {"id": f"DP{i:02}",
     "fuel": 10 + (i % 30),
     "medical": False,
     "technical_issue": False,
     "diplomatic_level": 4 + (i % 2),
     "arrival_time": 19.40 + i * 0.01}
    for i in range(50)
]

print(avions_diplomatic_50)

