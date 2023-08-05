from __future__ import annotations

from typing import List, Literal, Optional, Sequence, Union

from ..client import Client, Command, CommandArgs, SubCommand
from ..errors import Tile38Error
from ..models import (
    BoundsQuery,
    CircleQuery,
    Feature,
    GetQuery,
    HashQuery,
    ObjectQuery,
    Options,
    Polygon,
    QuadkeyQuery,
    TileQuery,
)
from ..responses import (
    BoundsNeSwResponses,
    CountResponse,
    FenceCommand,
    FenceDetect,
    HashesResponse,
    IdsResponse,
    JSONResponse,
    ObjectsResponse,
    PointsResponse,
)
from ..utils import flatten
from .executable import Compiled, Executable

Format = Literal["BOUNDS", "COUNT", "HASHES", "IDS", "OBJECTS", "POINTS"]
Output = Union[Sequence[Union[Format, int]]]


class Within(Executable):
    """WITHIN searches a key for objects that are fully contained within a given bounding area."""

    _key: str
    _command: Literal["WITHIN"]
    _hook = None
    _options: Options = {}
    _query: Union[
        CircleQuery,
        BoundsQuery,
        HashQuery,
        QuadkeyQuery,
        TileQuery,
        ObjectQuery,
        GetQuery,
    ]
    _output: Optional[Output] = None
    _all: bool = False
    _fence: bool = False
    _detect: Optional[List[FenceDetect]] = []
    _commands: Optional[List[FenceCommand]] = []

    def __init__(self, client: Client, key: str, hook=None) -> None:
        """__init__.

        Args:
            client (Client): client
            key (str): key to search in
            hook: Endpoint to send events to
                Options: AMQP, KAFKA, HTTPS/HTTP, SQS, MQTT, NATS, gRPC, Redis

        Returns:
            None
        """
        super().__init__(client)

        self.key(key)
        self._options = {}
        self._hook = hook

    def key(self, key: str) -> Within:
        """Set key to search in

        Args:
            key (str): key of a collection to search in

        Returns:
            Within
        """
        self._key = key

        return self

    def circle(self, lat: float, lon: float, radius: float) -> Within:
        """Define a circle as input bounding area for the within search.

        Args:
            lat (float): center latitude of circle
            lon (float): center longitude of circle
            radius (float): radius of circle

        Returns:
            Within
        """
        self._query = CircleQuery(lat=lat, lon=lon, radius=radius)

        return self

    def cursor(self, value: int) -> Within:
        """Cursor used to iterate though objects of the search results.

        Used for pagination through search results.

        Args:
            value (int): cursor value to start at, default: 0 if not set

        Returns:
            Within
        """
        self._options["cursor"] = value

        return self

    def limit(self, value: int) -> Within:
        """Limit the number of returned objects in a search.

        Also used for pagination through search results.

        Args:
            value (int): limit value, defaults to 100 if not set

        Returns:
            Within
        """
        self._options["limit"] = value

        return self

    def fence(self, flag: bool = True) -> Within:
        """Flag to indicate that the Within Query is used for a geo fence.

        Args:
            flag (bool): defaults to True if not set

        Returns:
            Within
        """
        self._fence = flag

        return self

    def detect(self, what: List[FenceDetect]) -> Within:
        """Option to filter the type of events in a geo fence.

        Args:
            what (List[FenceDetect]): what to detect in geo fence events.
                defaults to 'enter,exit,outside,inside,crosses' if not set

        Returns:
            Within
        """
        self._detect = what if len(what) > 0 else []

        return self

    def commands(self, which: Optional[List[FenceCommand]] = []) -> Within:
        """Option to filter what commands should be triggering a geo fence event.

        Args:
            which (Optional[List[FenceCommand]]): which commands trigger a geo fence event
                defaults to 'SET,DEL,JSET,JDEL' if not set

        Returns:
            Within
        """

        if which and len(which) > 0:
            self._commands = which

        return self

    def nofields(self, flag: bool = True) -> Within:
        """Option to explicitly not return fields in search results.

        Args:
            flag (bool): flag

        Returns:
            Within
        """
        self._options["nofields"] = flag

        return self

    def match(self, value: str) -> Within:
        """Match can be used to filtered objects considered in the search with a glob pattern.

        Args:
            value (str): value

        Returns:
            Within
        """
        self._options["match"] = value

        return self

    def sparse(self, value: int) -> Within:
        """Instead of returning all results of a search. Return a sparse result evenly distributed
        in the given search area. EXPERIMENTAL

        Args:
            value (int): values between 1 and 8

        Returns:
            Within
        """
        self._options["sparse"] = value

        return self

    def bounds(
        self, minlat: float, minlon: float, maxlat: float, maxlon: float
    ) -> Within:
        """Define a bounding as input bounding area for the within search.

        A bounding box is build from its most south-western and its most
        north-eastern point.

        Args:
            minlat (float): minimum latitude / south-west latitude
            minlon (float): minimum longitude / south-west longitude
            maxlat (float): maximum latitude / north-east latitude
            maxlon (float): maximum longitude / north-east longitude

        Returns:
            Within
        """
        self._query = BoundsQuery(
            minlat=minlat, minlon=minlon, maxlat=maxlat, maxlon=maxlon
        )

        return self

    def hash(self, geohash: str) -> Within:
        """Define a geohash as input bounding area for the within search.

        Args:
            geohash (str): geohash, eg. 'gcpvp'

        Returns:
            Within
        """
        self._query = HashQuery(geohash=geohash)

        return self

    def quadkey(self, quadkey: str) -> Within:
        """Define a quadkey as input bounding area for the within search.

        Args:
            quadkey (str): quadkey, eg. '120'

        Returns:
            Within
        """
        self._query = QuadkeyQuery(quadkey=quadkey)

        return self

    def tile(self, x: int, y: int, z: int) -> Within:
        """Define a tile as input bounding area for the within search.

        Args:
            x (int): x coordinate of the tile
            y (int): y coordinate of the tile
            z (int): z zoom level for the tile

        Returns:
            Within
        """
        self._query = TileQuery(x=x, y=y, z=z)

        return self

    def object(self, object: Union[Polygon, Feature]) -> Within:
        """Define an object as input bounding area for the within search.

        Args:
            object (Union[Polygon, Feature]): GeoJSON Feature or Polygon Geometry

        Returns:
            Within
        """
        self._query = ObjectQuery(object=object)

        return self

    def get(self, key: str, id: str) -> Within:
        """Define an object in a collection as bounding area for the within search.

        Args:
            key (str): key of the collection
            id (str): id of the object in the collection

        Returns:
            Within
        """
        self._query = GetQuery(key=key, id=id)

        return self

    def output(self, format: Format, precision: Optional[int] = None) -> Within:
        """Define an output format for query results.

        Args:
            format (Format): format,
                eg. 'OBJECTS', 'HASHES', 'BOUNDS', 'COUNT', 'IDS', 'POINTS'
            precision (Optional[int]): precision

        Returns:
            Within
        """
        if format == "OBJECTS":
            self._output = None
        elif format == "HASHES" and precision:
            self._output = [format, precision]
        elif format == "BOUNDS":
            self._output = [format]
        elif format == "COUNT":
            self._output = [format]
        elif format == "IDS":
            self._output = [format]
        elif format == "POINTS":
            self._output = [format]

        return self

    async def asObjects(self) -> ObjectsResponse:
        """Return query results as objects.

        Args:

        Returns:
            ObjectsResponse
        """
        self.output("OBJECTS")

        return ObjectsResponse(**(await self.exec()))

    async def asBounds(self) -> BoundsNeSwResponses:
        """Return query results as bounds.

        Args:

        Returns:
            BoundsNeSwResponses
        """
        self.output("BOUNDS")

        return BoundsNeSwResponses(**(await self.exec()))

    async def asHashes(self, precision: int) -> HashesResponse:
        """Return query results as geohashes.

        Args:
            precision (int): precision of the returned geohash

        Returns:
            HashesResponse
        """
        self.output("HASHES", precision)

        return HashesResponse(**(await self.exec()))

    async def asCount(self) -> CountResponse:
        """Return query results as count only.

        Args:

        Returns:
            CountResponse
        """
        self.output("COUNT")

        return CountResponse(**(await self.exec()))

    async def asIds(self) -> IdsResponse:
        """Return query results as object ids only.

        Args:

        Returns:
            IdsResponse
        """
        self.output("IDS")

        return IdsResponse(**(await self.exec()))

    async def asPoints(self) -> PointsResponse:
        """Return query results as points.

        Args:

        Returns:
            PointsResponse
        """
        self.output("POINTS")

        return PointsResponse(**(await self.exec()))

    def __compile_options(self) -> CommandArgs:
        """__compile_options.

        Args:

        Returns:
            CommandArgs
        """
        commands = []

        # raises mypy: TypedDict key must be string literal
        # open PR: https://github.com/python/mypy/issues/7867
        for k in self._options.keys():
            if isinstance(self._options[k], bool):  # type: ignore
                commands.append(k.upper())
            elif self._options[k]:  # type: ignore
                commands.extend([k.upper(), self._options[k]])  # type: ignore
            elif self._options[k] == 0:  # type: ignore
                commands.extend([k.upper(), self._options[k]])  # type: ignore

        return commands

    def __compile_fence(self) -> CommandArgs:
        """__compile_fence

        Args:

        Returns:
            CommandArgs
        """
        return (
            [
                SubCommand.FENCE.value,
                *(
                    [SubCommand.DETECT.value, ",".join(self._detect)]
                    if self._detect
                    else []
                ),
                *(
                    [SubCommand.COMMANDS.value, ",".join(self._commands)]
                    if self._commands
                    else []
                ),
            ]
            if self._fence
            else []
        )

    def compile(self) -> Compiled:
        """compile

        Args:

        Returns:
            Compiled
        """
        compiled = [
            Command.WITHIN.value,
            [
                self._key,
                *(self.__compile_options()),
                *(self.__compile_fence()),
                *(self._output if self._output else []),
                *(self._query.get()),
            ],
        ]

        if self._hook:
            command, args = self._hook.compile()
            response = [command, [*(args), *(flatten(compiled))]]
            return response

        return compiled

    async def activate(self) -> JSONResponse:  # type: ignore
        """Activate is used in SetHook to activate a geo-fenced search.

        Args:

        Returns:
            JSONResponse
        """
        if self._hook:
            return JSONResponse(**(await self.client.command(*self.compile())))
        else:
            raise Tile38Error("No hook to activate")
