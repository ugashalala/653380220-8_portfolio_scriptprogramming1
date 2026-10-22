# labxAdvance_week8/src/data_agent.py
import os
import json
import datetime
import sys
from utils import setup_logging, log_audit_entry, ensure_directory_exists
from csv_tasks import CSVTasks
from json_tasks import JSONTasks
from conversion_tasks import ConversionTasks

logger = setup_logging(__name__)

class DataAgent:
    """Core Agent for orchestrating data pipeline tasks."""
    def __init__(self, config):
        self.config = config
        self.audit_log = []
        self.data_store = {}
        self.start_time = datetime.datetime.now()
        self.csv_tasks = CSVTasks()
        self.json_tasks = JSONTasks()
        self.conversion_tasks = ConversionTasks()
        logger.info("Data Agent initialized.")

    def _get_data(self, key):
        return self.data_store.get(key)

    def _set_data(self, key, data):
        if key:
            self.data_store[key] = data

    def _process_task(self, task):
        task_type = task.get("type")
        task_name = task.get("name", task_type)
        input_key = task.get("input_data_key")
        output_key = task.get("output_data_key")

        logger.info(f"Executing task: {task_name} ({task_type})")
        log_audit_entry(self.audit_log, "INFO", f"Starting task '{task_name}'", task_type)

        input_data = self._get_data(input_key) if input_key else None
        output_data = None
        success = False

        try:
            if task_type == "load_csv":
                output_data = self.csv_tasks.load_csv(task.get("file_path"))
                success = output_data is not None
            elif task_type == "save_csv":
                success = self.csv_tasks.save_csv(input_data, task.get("file_path"), task.get("fieldnames"))
            elif task_type == "transform_csv_aggregate":
                output_data = self.csv_tasks.transform_csv_aggregate(input_data, task.get("group_by_field"), task.get("aggregate_field"), task.get("aggregate_type", "sum"))
                success = output_data is not None
            elif task_type == "filter_csv":
                output_data = self.csv_tasks.filter_csv(input_data, task.get("filter_field"), task.get("operator"), task.get("value"))
                success = output_data is not None
            elif task_type == "load_json":
                output_data = self.json_tasks.load_json(task.get("file_path"))
                success = output_data is not None
            elif task_type == "save_json":
                success = self.json_tasks.save_json(input_data, task.get("file_path"), task.get("indent", 2))
            elif task_type == "update_json_data":
                output_data = self.json_tasks.update_json_data(input_data, task.get("updates", []))
                success = output_data is not None
            elif task_type == "query_json_data":
                output_data = self.json_tasks.query_json_data(input_data, task.get("path"))
                success = True
            elif task_type == "csv_to_json_conversion":
                output_data = self.conversion_tasks.csv_to_json(input_data)
                success = output_data is not None

            if success:
                if output_data is not None:
                    self._set_data(output_key, output_data)
                log_audit_entry(self.audit_log, "SUCCESS", f"Task '{task_name}' completed.", task_type)
            else:
                log_audit_entry(self.audit_log, "ERROR", f"Task '{task_name}' failed.", task_type)
        except Exception as e:
            log_audit_entry(self.audit_log, "ERROR", f"Error in task '{task_name}': {e}", task_type)

    def generate_audit_report(self, output_dir="reports"):
        ensure_directory_exists(output_dir)
        filename = f"audit_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(output_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_log, f, indent=4, ensure_ascii=False)
        logger.info(f"Audit report written to: {path}")

    def run(self):
        for task in self.config.get("tasks", []):
            self._process_task(task)
        self.generate_audit_report()