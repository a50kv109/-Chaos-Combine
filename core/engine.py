"""
Chaos-Combine Engine v1.0
Оркестратор методологических инструментов
"""

import yaml
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime


class ChaosEngine:
    """
    Главный движок Chaos-Combine
    Загружает конфигурации, вызывает промпты, формирует отчёты
    """
    
    def __init__(self, config: str = "default.yaml"):
        self.config = self._load_config(config)
        self.prompts = self._load_prompts()
        self.templates = self._load_templates()
        self.version = "1.0.0"
        self.timestamp = datetime.now().isoformat()
    
    def _load_config(self, config: str) -> Dict:
        """Загрузка конфигурации"""
        config_path = Path(__file__).parent.parent / "config" / config
        if not config_path.exists():
             return {"mode": "default", "analysis_depth": "medium"}
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_prompts(self) -> Dict:
        """Загрузка библиотеки промптов"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts = {}
        if prompts_dir.exists():
            for category in prompts_dir.iterdir():
                if category.is_dir():
                    for prompt_file in category.glob("*.md"):
                        key = f"{category.name}/{prompt_file.stem}"
                        with open(prompt_file, 'r') as f:
                            prompts[key] = f.read()
        return prompts
    
    def _load_templates(self) -> Dict:
        """Загрузка библиотеки шаблонов"""
        templates_dir = Path(__file__).parent.parent / "templates"
        templates = {}
        if templates_dir.exists():
            for category in templates_dir.iterdir():
                if category.is_dir():
                    for template_file in category.glob("*.md"):
                        key = f"{category.name}/{template_file.stem}"
                        with open(template_file, 'r') as f:
                            templates[key] = f.read()
        return templates
    
    def audit(self, system_description: str, config: Optional[str] = None) -> Dict[str, Any]:
        return self._run("audit/architecture_audit", system_description, config)
    
    def reduce(self, component_description: str, config: Optional[str] = None) -> Dict[str, Any]:
        return self._run("reduction/sol_reduction", component_description, config)
    
    def red_team(self, hypothesis_description: str, config: Optional[str] = None) -> Dict[str, Any]:
        return self._run("audit/red_team_audit", hypothesis_description, config)
    
    def semantic_drift(self, term: str, languages: List[str] = None, config: Optional[str] = None) -> Dict[str, Any]:
        if languages is None:
            languages = ["en", "ru", "zh", "de", "fr"]
        content = f"Term: {term}\nLanguages: {', '.join(languages)}"
        return self._run("experiments/semantic_drift", content, config)
    
    def compare(self, architecture_a: str, architecture_b: str, config: Optional[str] = None) -> Dict[str, Any]:
        content = f"Architecture A: {architecture_a}\nArchitecture B: {architecture_b}"
        return self._run("comparison/two_heroes", content, config)
    
    def _run(self, prompt_key: str, content: str, config: Optional[str]) -> Dict[str, Any]:
        prompt = self.prompts.get(prompt_key)
        if not prompt:
            return {"error": f"Prompt not found: {prompt_key}"}
        
        return {
            "version": self.version,
            "timestamp": self.timestamp,
            "prompt": prompt_key,
            "config": config or self.config,
            "result": f"REQUEST to LLM: {prompt[:100]}... [Content: {content[:50]}...]",
            "status": "PENDING"
        }
    
    def generate_report(self, data: Dict) -> str:
        template = self.templates.get("reports/engineering_report")
        if not template:
            return str(data)
        return template.replace("{{data}}", json.dumps(data, indent=2, ensure_ascii=False))
    
    def get_version(self) -> str:
        return self.version
    
    def get_config(self) -> Dict:
        return self.config

if __name__ == "__main__":
    engine = ChaosEngine()
    print(f"Chaos-Combine Engine v{engine.get_version()} initialized.")
