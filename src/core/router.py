from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional
from fastapi import APIRouter, FastAPI
import logging

logger = logging.getLogger(__name__)


"""
FastAPI 확장 모듈
"""
class SemtleAPI(FastAPI):
    def __init__(self, **kwargs):
        """
        FastAPI를 확장한 SemtleAPI 클래스
        - kwargs에 'disable_api_doc'이 True이면 있으면 API 문서(docs, redoc)를 비활성화
        """
        if kwargs.get('disable_api_doc', None):
            kwargs.update({"redoc_url": None, "docs_url": None})
        super().__init__(**kwargs)
    
    def use_router_manager(self, base_path: str):
        """RouterManager를 사용하여 라우터를 로드"""
        router_manager = RouterManager(self, base_path)
        router_manager.load_routers()
    
    def use(self, extension_module, *args, **kwargs):
        """ 외부 확장 모듈 사용 """
        extension_module.use(self, *args, **kwargs)
    

"""
라우터 확장 모듈
"""
class RouterManager:
    def __init__(self, app: FastAPI, base_path: str):
        self.app = app
        self.base_path = base_path
    
    def _get_module_name(self, path: Path) -> str:
        ''' 파일 경로로부터 모듈 이름 생성('src/api/auth/auth_control.py' -> 'src.api.auth.auth_control') '''
        paths = []
        if path.name != '__init__.py':
            paths.append(path.stem)
        while True:
            path = path.parent
            if not path or not path.is_dir():
                break

            inits = [f for f in path.iterdir() if f.name == '__init__.py']
            if not inits:
                break

            paths.append(path.stem)

        module_name = '.'.join(reversed(paths))
        logger.info(f"=>> 파일 경로로부터 라우터 이름 생성 : {module_name}")
        return module_name

    def _load_module(self, module_name: str, attr_name: str) -> Optional[APIRouter]:
        """ 모듈 동적 임포트 및 로드 """
        logger.info(f"=>> 라우터 로드 중 -> module_name : {module_name}, attr_name : {attr_name}")
        module = __import__(module_name, fromlist=[attr_name])
        return getattr(module, attr_name, None)


    def load_routers(self):
        """ base_path 하위의 모든 *_control.py 파일에서 라우터 로드 """
        api_router = APIRouter()
        for path in Path(self.base_path).glob("**/*_ctl.py"):
            module_name = self._get_module_name(path)
            logger.info(f"로드 중: {module_name}")
            router = self._load_module(module_name, "router")
            if router:
                api_router.include_router(router)
        self.app.include_router(api_router)
        logger.info("모든 라우터가 성공적으로 추가되었습니다.")