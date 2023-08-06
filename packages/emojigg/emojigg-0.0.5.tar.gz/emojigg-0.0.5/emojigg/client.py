import aiohttp
from attr import has
from .http import HTTP
from .pack import Pack
from .emoji import Emoji
from .errors import WrongType

from typing import (
    Optional, 
    List, 
    Union
)


class Client(HTTP):
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        super().__init__(session=session or aiohttp.ClientSession())

    async def get_pack_from(
        self, 
        attr: str, 
        value: str,
        *,
        packs: List[Pack] = []
    ) -> Union[None, Emoji]:
        """
        Get pack from an attribute of the Pack.
        
        Parameters
        ----------
        attr: str
            The attribute of the Pack you want to search for
        value: str
            The vlaue you want the attribute to be.
        packs: List[Pack]
            The optional list of packs to search through. If none is specified a request will be made to get all packs.
            
        Returns
        -------
        Optional[Pack]
        """
        packs = await self.fetch_packs() if not packs else packs
        if not hasattr(packs[0], attr):
            raise WrongType(f"class Pack does not have attribute {attr}")
        
        for pack in packs:
            if getattr(pack, attr) == value:
                return pack
        
        return None

    