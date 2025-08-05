import time
import json
import os

__all__ = ["get_sample_id", "set_sample_id", "log_args_result_and_time"]

sample_id = None
log_dir = None

def get_sample_id():
    global sample_id
    return sample_id

def set_sample_id(value: int):
    global sample_id
    sample_id = value

def set_log_dir(value: str):
    global log_dir
    log_dir = value

def log_args_result_and_time():
    def create_decorator(func):
        def log_args_result_and_time(*args):
            if sample_id is None:
                raise ValueError("Sample ID is not set. Please set it using set_sample_id() before using this decorator.")
            if log_dir is None:
                raise ValueError("Log directory is not set. Please set it using set_log_dir() before using this decorator.")
                
            output_file_name = f"{log_dir}/{sample_id}_{func.__name__}.json"

            if os.path.exists(output_file_name):
                raise FileExistsError(f"File {output_file_name} already exists. Please delete it and try again.")
            
            
            start_time = time.time()
            result = func(*args)
            end_time = time.time()

            log_data = {
                "sample_id": sample_id,
                "args": args,
                "time_taken": end_time - start_time,
                "output": result,
                "func_name": func.__name__,
            }

            if func.__doc__:
                log_data["func_doc"] = func.__doc__

            
            with open(output_file_name, "w") as f:
                json.dump(log_data, f, indent=4)

            return result
        
        return log_args_result_and_time
    
    return create_decorator
