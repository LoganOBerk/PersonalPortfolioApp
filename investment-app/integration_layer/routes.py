import secrets

from fastapi import APIRouter, HTTPException

from common.errors import ServiceError, ValidationError
from .frontendapi import FrontendApi
from .pydmodels import LogoutRequest, CredsRequest, FundsRequest, PortfolioRequest, TransactionRequest, StockData, PortfolioData, UserData 

router = APIRouter()

frontend_api : FrontendApi

active_sessions : dict = {}


# INPUT:
#   -api(FrontendApi); functional interface
# OUTPUT: None
# PRECONDITION:
#   -api; is populated with a service and validator
# POSTCONDITION:
#   -frontend_api; passed api is assigned to global module memory
# RAISES: None
def connect(api : FrontendApi) -> None:
    global frontend_api
    frontend_api = api


# INPUT: None
# OUTPUT:
#   -session_id(str); a random string
# PRECONDITION: None
# POSTCONDITION:
#   -session_id; a random string is generated, is unique from any id in active sessions
# RAISES: None
def generate_session_id() -> str:
    session_id = secrets.token_hex(32)

    while session_id in active_sessions:
        session_id = secrets.token_hex(32)

    return session_id


# INPUT:
#   -user(User); a user account
# OUTPUT:
#   -session_id(str); a random string
# PRECONDITION:
#   -user; is fully populated
# POSTCONDITION:
#   -active_sessions; a generated session id is keyed to the user establishing their session
# RAISES: None
def start_session(user) -> str:
    session_id = generate_session_id()
    active_sessions[session_id] = user
    return session_id


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/register", status_code = 201)
def register(req : CredsRequest):

    creds = (req.login, req.password)

    try:

        frontend_api.create_account(creds)
        
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))


    return {"message" : "account created"}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/login", status_code = 200)
def login(req : CredsRequest):

    creds = (req.login, req.password)

    try:

        user = frontend_api.find_account(creds)

    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 404, detail = str(e))


    session_id = start_session(user)
    return {"session_id" : session_id, "user" : UserData.convert(user)}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/logout")
def logout(req : LogoutRequest):
    active_sessions.pop(req.session_id, None)
    return {"message" : "logged out"}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/fund")
def fund(req : FundsRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:

        frontend_api.fund_account(user, req.funds_requested)
       
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


    return {"user" : UserData.convert(user)}
    

# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/portfolio/create", status_code=201)
def create_portfolio(req : PortfolioRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:

        frontend_api.create_portfolio(user, req.name)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


    return {"user" : UserData.convert(user)}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/portfolio/remove")
def remove_portfolio(req : PortfolioRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:

        frontend_api.remove_portfolio(user, req.name)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))


    return {"user" : UserData.convert(user)}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/buy")
def buy(req : TransactionRequest):
    user = active_sessions.get(req.session_id)
    shares_requested = (req.ticker, req.quantity)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    portfolio = user.portfolios.get(req.portfolio_name)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    try:

        frontend_api.execute_buy(user, portfolio, shares_requested)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


    return {"portfolio" : PortfolioData.convert(portfolio)}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.post("/sell")
def sell(req : TransactionRequest):
    user = active_sessions.get(req.session_id)
    shares_requested = (req.ticker, req.quantity)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    portfolio = user.portfolios.get(req.portfolio_name)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    try:

        frontend_api.execute_sell(user, portfolio, shares_requested)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


    return {"portfolio" : PortfolioData.convert(portfolio)}


# INPUT:
# OUTPUT:
# PRECONDITION:
# POSTCONDITION:
# RAISES:
@router.get("/user")
def get_user(session_id : str):
    user = active_sessions.get(session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return {"user": UserData.convert(user)}