def cluster_rows(blocks, y_threshold=15):
    rows = []

    for block in sorted(blocks, key=lambda b: b["bbox"]["y"]):
        placed = False

        for row in rows:
            if abs(row[0]["bbox"]["y"] - block["bbox"]["y"]) < y_threshold:
                row.append(block)
                placed = True
                break

        if not placed:
            rows.append([block])

    return rows
