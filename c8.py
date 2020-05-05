with open("8.txt") as f:
    repititions = []
    for line in f:
        encrypted = bytes.fromhex(line.strip())
        chunks = [encrypted[i : i + 16] for i in range(0, len(encrypted), 16)]
        repititions.append({"text": encrypted, "reps": len(chunks) - len(set(chunks))})

    ans = sorted(repititions, key=lambda x: x["reps"], reverse=True)[0]
    print(ans["text"])
    print(ans["reps"])
    # encrypted = f.read()
    # encrypted = bytes.fromhex(encrypted).decode("ascii")
    # print(encrypted)
