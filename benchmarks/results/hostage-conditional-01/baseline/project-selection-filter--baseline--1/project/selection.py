def visible(records, *, include_archived=False, project_ids=None):
    selected_projects = None if project_ids is None else set(project_ids)
    return [
        row for row in records
        if (include_archived or not row.get("archived"))
        and (selected_projects is None or row.get("project_id") in selected_projects)
    ]
