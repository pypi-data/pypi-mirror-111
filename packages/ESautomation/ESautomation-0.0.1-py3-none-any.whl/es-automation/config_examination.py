"""
Check the format and content of the config
"""
import json
from mlaas_tools2.feature_tool import FeatureBase

class config_examination(FeatureBase):
    """
    efk_setup.json config pre-examination.
    """
    def __init__(self):
        super().__init__()

    def config_format_check(self, content: str):
        """
        Check config is JSON format, if not then raise error
        Params
        - content: (str) the content of the config
        """
        try:
            doc = json.dumps(content)
        except TypeError as e:
            self.logger.error("Config check: Not valid JSON format", exc_info=True)
            raise e
        if not doc.startswith("{") and not doc.endswith("}"):
            raise ValueError("Not valid JSON format ")

    def read_config(self):
        """
        Read efk_setup.json
        """
        default_path = "efk_setup.json"
        try:
            with open(default_path) as f:
                content = json.load(f)
                return content
        except ValueError as e:
            self.logger.error("Config check: Not valid JSON format", exc_info=True)
            raise e
        except Exception as e:
            raise e

    def check_owner(self, content: str):
        """
        Check config owner is da or de, if not then raise error
        """
        if content.get("owner") not in ["da", "de"]:
            self.logger.error("Owner is invalid")
            raise ValueError("Owner is invalid")

    def config_examine_run(self, content: str):
        """
        Config examination main run 
        """
        self.config_format_check(content)
        self.check_owner(content)
