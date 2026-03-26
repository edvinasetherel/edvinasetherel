import pydantic

class Profile(pydantic.BaseModel):
    title: str
    taglines: list[str]

class Link(pydantic.BaseModel):
    name: str
    url: str

class Config(pydantic.BaseModel):
    profile: Profile
    links: list[Link]
