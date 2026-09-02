def update_leaderboard(existing_entries=None, new_entries=None, limit=10):
    all_entries = []
    if existing_entries is not None:
        all_entries.extend(existing_entries)
    if new_entries is not None:
        all_entries.extend(new_entries)

    seen_game_ids = set()
    valid_entries = []

    for entry in all_entries:
        if not isinstance(entry, dict):
            continue

        game_id = entry.get('game_id')
        player_name = str(entry.get('player_name', '')).strip()
        completion_time = entry.get('completion_time')
        difficulty = str(entry.get('difficulty', '')).strip().lower()
        hints_used = entry.get('hints_used')

        if game_id is not None:
            game_key = str(game_id)
            if game_key in seen_game_ids:
                continue
            seen_game_ids.add(game_key)

        if not player_name:
            continue

        try:
            completion_seconds = int(completion_time)
            hint_count = int(hints_used)
        except (TypeError, ValueError):
            continue

        if completion_seconds < 0 or hint_count < 0:
            continue
        if difficulty not in {'easy', 'medium', 'hard'}:
            continue

        valid_entries.append({
            'game_id': str(game_id) if game_id is not None else '',
            'player_name': player_name,
            'completion_time': completion_seconds,
            'difficulty': difficulty,
            'hints_used': hint_count,
        })

    sorted_entries = sorted(
        valid_entries,
        key=lambda item: (item['completion_time'], item['hints_used'], item['player_name'])
    )
    return sorted_entries[:limit]
