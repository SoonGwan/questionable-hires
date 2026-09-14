from flags import read_flag


def worker_options(env):
    return {"trace": read_flag(env, "TRACE"), "retries": 3}
