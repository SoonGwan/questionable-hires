def visible(records, *, include_archived=False, project_ids=None):
    project_ids = None if project_ids is None else tuple(project_ids)
    return [
        row for row in records
        if (include_archived or not row.get("archived"))
        and (project_ids is None or row.get("project_id") in project_ids)
    ]
