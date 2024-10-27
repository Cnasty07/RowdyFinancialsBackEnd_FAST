from fastapi import FastAPI, Depends
from propelauth_fastapi import init_auth, init_base_auth, User , TokenVerificationMetadata


app = FastAPI()
# auth = init_auth("https://0586364.propelauthtest.com","MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4tdMs4QaBmGDmIpIAIj6W5KMVOt/fch3jj9vuMxmI47aXpj/xSB1p7/7DTfLaorPffFhaNccc0veLmAcVhh5KLDW2SgcIC7VMlcJX+UmqKOSalgd5qXnqRKwfar0e5L77hC3emF3jL7vY5begyDa+TmOCK5N9q0TvGmcsWhaxw/OTAkbdwHjlhQwciNx2osm9YX0gETa0S1usFh5eSleekAWlOh4ZByNpRYt1rn3wihe1zh93I4JG+J76ZSM5pGqKk5C3+HYw0h+cSu0ZIhA1jIOr+GU2UsLbpTjzwgE64txyzAUgpZ+qzMZm4qRdqHV22GIZL07Oir0+uT0hyPU5wIDAQAB") # need to add 
#  chnast01 access eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjkzNGU1NjlkLWI5MGItNGQwNi1iMmMzLWEzMWJiYmVjYWRmNSJ9.eyJzdWIiOiJjOTdhY2Y4YS01MDRmLTRjNzEtOWY5Ny00ODlmY2EwYmYxZDgiLCJpYXQiOjE3MzAwMDQ1NDgsImV4cCI6MTczMDA5MDk0OCwidXNlcl9pZCI6ImM5N2FjZjhhLTUwNGYtNGM3MS05Zjk3LTQ4OWZjYTBiZjFkOCIsImlzcyI6Imh0dHBzOi8vMDU4NjM2NC5wcm9wZWxhdXRodGVzdC5jb20iLCJlbWFpbCI6ImNobmFzdDAxQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJDaHJpcyIsImxhc3RfbmFtZSI6Ik5hc3Rhc2kiLCJvcmdfaWRfdG9fb3JnX21lbWJlcl9pbmZvIjp7fX0.lZf7cL4p1N_7OApd7htAgHUkkoePclg6SIfgvOB946gln4u9L7oIOkARxUFD01mk_gJXUnrjHGm4CqQiUOiShlIkqC2Xtpazri_ZJElD-BWb8ObY9UOiIgHLE94O4PT_H3Zez214xJETLHS2pl2hpcG_QX-sxhItT02JkR_uoiwwEW9j50Sr0vYYeyD6Qgcdf7BXJx87aujXmp-HnfVk_4XP5dHIZzL5JssOlXLKlP_JBlFsSvHX_4vqfXqCf8NKChvwZU40pN58zv9rd9Vn5Ni9-A9fEgrU3QoERfD0bZBtnuVPUSYO7Ak8Ic3lYhAGukmQGoSqN8eaGV8Vo4vQwQ

auth = init_auth(auth_url="https://0586364.propelauthtest.com",api_key="ebcccafcdab1720e7ed2831c693d7f43e45d16289144d0cced610832d530ee30011868662168683dc87276750d6c27f3",debug_mode=True)


# checks who user is (make sure to get user access token)
@app.get("/api/v1/whoami")
async def read_root(current_user: User = Depends(auth.require_user)):
    return {"Hello": f"{current_user.user_id}"}


# -- Accounts Endpoints -- 
# needs to authenticate token and then retrieve users balances
@app.get("/api/v1/get/accounts")
async def get_accounts(current_user: User = Depends(auth.require_user)):
    #
    return {"accounts": {"checkings": int , "savings": int}}

@app.get("api/v1/update/accounts/transfer")
async def transfer_accounts(current_user: User = Depends(auth.require_user)):
    #
    return {}


# -- Profile Endpoints -- 
@app.get("/api/v1/get/profile")
async def get_profile(current_user: User = Depends(auth.require_user)):
    #
    return {current_user.user_id: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}

# updates profile POST (sends to db to update)
@app.post("/api/v1/update/profile")
async def get_profile(updates: object, current_user: User = Depends(auth.require_user)):
    
    return {current_user: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}
