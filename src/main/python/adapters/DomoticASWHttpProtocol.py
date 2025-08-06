from fastapi import Body, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from domain.SmartWindowAgent import SmartWindowAgent
from domain.SmartWindow import InvalidAngleError, InvalidOperationError, SmartWindow
from domoticASW.DomoticASWProtocol import ActionId, DeviceAction, DevicePropertyWithSetter, DevicePropertyWithTypeConstraint, DeviceRegistration, Type, TypeConstraintEnum, TypeConstraintIntRange, TypeConstraintNone
from ports.ServerProtocol import ServerAddress

def OkResponse(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": message}
    )

def BadRequest(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"cause": message}
    )

def NotFound(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"cause": message}
    )

# === ENDPOINTS ===

def create_server(smart_window_agent: SmartWindowAgent) -> FastAPI:
    app = FastAPI()

    def get_smart_window_agent() -> SmartWindowAgent:
        return smart_window_agent
    
    @app.get("/check-status")
    def check_status():
        return OkResponse(message="Washing machine is online")

    @app.post("/execute/{action}")
    def execute_action(action: str, body: dict = Body(...), smart_window_agent: SmartWindowAgent = Depends(get_smart_window_agent)):
        window = smart_window_agent.smart_window
        try:
            match action:
                case "open":
                    window.open()
                case "tilt":
                    window.tilt(body.get("input"))
                case "close":
                    window.close()
                case _:
                    return NotFound(message=f"Action '{action}' not found")
        except (InvalidOperationError, InvalidAngleError) as e:
            return BadRequest(message=str(e))
        return OkResponse(message=f"Action '{action}' executed successfully")

    @app.post("/register")
    def register_device(request: Request, body: dict = Body(...), smart_window_agent: SmartWindowAgent = Depends(get_smart_window_agent)):
        server_host = request.client.host
        server_port = body.get("serverPort")
        smart_window_agent.set_server_address(ServerAddress(server_host, server_port))
        print(f"SERVER: Machine agent start to run")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=deviceRegistration(smart_window_agent.smart_window).model_dump()
        )
    
    return app


def deviceRegistration(smart_window: SmartWindow) -> DeviceRegistration:
    return DeviceRegistration(
        id=smart_window.id,
        name=smart_window.name,
        properties=[
            DevicePropertyWithTypeConstraint(
                id="state",
                name="State",
                value=smart_window.state.name,
                typeConstraints=TypeConstraintEnum(values=["Idle", "Moving"])
            ),
            DevicePropertyWithTypeConstraint(
                id="position",
                name="Position",
                value=smart_window.position,
                typeConstraints=TypeConstraintEnum(values=["Open", "Tilt", "Closed"])
            ),
            DevicePropertyWithSetter(
                id="angle",
                name="Angle",
                value=smart_window.angle,
                setterActionId=ActionId("tilt")
            )
        ],
        actions=[
            DeviceAction(
                id="open",
                name="Open Window",
                description="Fully opens the window",
                inputTypeConstraints=TypeConstraintNone(type=Type.VOID)
            ),
            DeviceAction(
                id="tilt",
                name="Tilt Window",
                description="Regulates the window angle between 0 and 90 degrees.",
                inputTypeConstraints=TypeConstraintIntRange(min=0, max=90)
            ),
            DeviceAction(
                id="close",
                name="Close Window",
                description="Closes the window",
                inputTypeConstraints=TypeConstraintNone(type=Type.VOID)
            )
        ],
        events=["opened", "closed"]
    )
