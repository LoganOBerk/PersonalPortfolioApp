import secrets

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from common.errors import ServiceError, ValidationError
from .frontendapi import FrontendApi

router = APIRouter()

frontend : FrontendApi

active_sessions : dict = {}

def init(frontend_api : FrontendApi) -> None:
    global frontend
    frontend = frontend_api

def generate_session_id() -> str:
    return secrets.token_hex(32)

class LogoutRequest(BaseModel):
    session_id: str

class CredsRequest(BaseModel):
    login: str
    password: str

class FundsRequest(BaseModel):
    session_id: str
    funds_requested: float

class PortfolioRequest(BaseModel):
    session_id: str
    name: str

class TransactionRequest(BaseModel):
    session_id: str
    portfolio_name: str
    ticker: str
    quantity: int


class StockData(BaseModel):
    ticker: str
    quantity: int

class PortfolioData(BaseModel):
    name: str
    stocks: dict[str, StockData]

    @classmethod
    def convert(cls, portfolio):
        return cls(
            name=portfolio.name,
            stocks={
                ticker: StockData(ticker=ticker, quantity=qty)
                for ticker, qty in portfolio.stocks.items()
            }
        )
       

class UserData(BaseModel):
    login: str
    balance: float
    portfolios: dict[str, PortfolioData]

    @classmethod
    def convert(cls, user):
        return cls(
            login=user.login,
            balance=user.balance,
            portfolios={
                name: PortfolioData.convert(portfolio)
                for name, portfolio in user.portfolios.items()
            }
        )

@router.post("/register", status_code = 201)
def register(req : CredsRequest):

    creds = (req.login, req.password)

    try:

        frontend.create_account(creds)
        return {"message" : "account created"}

    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.post("/login", status_code = 200)
def login(req : CredsRequest):

    creds = (req.login, req.password)

    try:

        user = frontend.find_account(creds)
        session_id = generate_session_id()
        active_sessions[session_id] = user
        return {"session_id" : session_id, "user" : UserData.convert(user)}

    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except ServiceError as e:
        raise HTTPException(status_code = 404, detail = str(e))


@router.post("/logout")
def logout(req : LogoutRequest):
    active_sessions.pop(req.session_id, None)
    return {"message" : "logged out"}


@router.post("/fund")
def fund(req : FundsRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:

        frontend.fund_account(user, req.funds_requested)
        return {"user" : UserData.convert(user)}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/portfolio/create", status_code=201)
def create_portfolio(req : PortfolioRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:
        frontend.create_portfolio(user, req.name)
        return {"user" : UserData.convert(user)}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/remove")
def remove_portfolio(req : PortfolioRequest):
    user = active_sessions.get(req.session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    try:

        frontend.remove_portfolio(user, req.name)
        return {"user" : UserData.convert(user)}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/buy")
def buy(req : TransactionRequest):
    user = active_sessions.get(req.session_id)
    shares_requested = (req.ticker, req.quantity)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    portfolio = user.portfolios.get(req.portfolio_name)

    try:
        frontend.execute_buy(user, portfolio, shares_requested)
        return {"portfolio" : PortfolioData.convert(portfolio)}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sell")
def sell(req : TransactionRequest):
    user = active_sessions.get(req.session_id)
    shares_requested = (req.ticker, req.quantity)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    portfolio = user.portfolios.get(req.portfolio_name)

    try:

        frontend.execute_sell(user, portfolio, shares_requested)
        return {"portfolio" : PortfolioData.convert(portfolio)}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user")
def get_user(session_id : str):
    user = active_sessions.get(session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")

    return {"user": UserData.convert(user)}