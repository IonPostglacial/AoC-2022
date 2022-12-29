TileType[,] ParseMap(string[] lines)
{
    var height = lines.Length;
    var width = lines[0].Length;
    var map = new TileType[width, height];
    for (var y = 0; y < height; y++)
    {
        for (var x = 0; x < width; x++)
        {
            if (x >= lines[y].Length)
            {
                map[x, y] = TileType.Empty;
                continue;
            }
            map[x, y] = lines[y][x] switch
            {
                ' ' => TileType.Empty,
                '.' => TileType.Open,
                '#' => TileType.Solid,
                _ => throw new System.Diagnostics.UnreachableException(),
            };
        }
    }
    return map;
}

List<Order> ParseOrders(string orderline)
{
    var orders = new List<Order>();
    var isMove = false;
    var numStart = 0;
    var numEnd = 0;
    for (var i = 0; i < orderline.Length; i++)
    {
        var c = orderline[i];
        if (c == 'R' || c == 'L')
        {
            if (isMove)
            {
                numEnd = i;
                var n = int.Parse(orderline.Substring(numStart, numEnd - numStart));
                orders.Add(new Order(Rotations.None, n));
            }
            isMove = false;
            orders.Add(new Order(c == 'R' ? Rotations.Clockwise : Rotations.Counterclockwise, 0));
        }
        else if (isMove == false)
        {
            isMove = true;
            numStart = i;
            numEnd = i;
        }
    }
    numEnd = orderline.Length;
    if (isMove && numStart < numEnd)
    {
        var n = int.Parse(orderline.Substring(numStart, numEnd - numStart));
        orders.Add(new Order(Rotations.None, n));
    }
    return orders;
}

if (args.Length == 0)
{
    Console.WriteLine("part 1 or 2 ?");
}

var input = System.IO.File.ReadAllText("input.txt");
var parts = input.Split($"{Environment.NewLine}{Environment.NewLine}").ToArray();
var map = ParseMap(parts[0].Split($"{Environment.NewLine}"));
var orders = ParseOrders(parts[1]);
var startx = 0;
while (map[startx, 0] == TileType.Empty)
    startx++;
var player = new Player(Directions.Right, (startx, 0));
IPuzzle puzzle;
if (args[0] == "1")
{
    puzzle = new Puzzle(map);
}
else
{
    puzzle = new Puzzle2(parts[0].Split($"{Environment.NewLine}"));
}
foreach (var order in orders)
{
    player = puzzle.Execute(order, player);
}
Console.WriteLine($"{puzzle.Password(player)}");

enum TileType { Empty, Open, Solid }
enum Rotations { None, Clockwise, Counterclockwise }
enum Directions { Right, Down, Left, Up }
readonly record struct Player(Directions Direction, (int x, int y) Position) { }
record struct Order(Rotations Rotation, int Move) { }

interface IPuzzle
{
    Player Execute(Order order, Player player);
    int Password(Player player);
}

class Puzzle : IPuzzle
{
    TileType[,] Map;

    public Puzzle(TileType[,] map)
    {
        Map = map;
    }

    public Player Execute(Order order, Player player)
    {
        return ExecuteTurn(order, Map, ExecuteMove(order, Map, player));
    }

    Player ExecuteTurn(Order order, TileType[,] map, Player player)
    {
        return order.Rotation switch
        {
            Rotations.None => player,
            Rotations.Clockwise => player with
            {
                Direction = player.Direction == Directions.Up ? Directions.Right : player.Direction + 1
            },
            Rotations.Counterclockwise => player with
            {
                Direction = player.Direction == Directions.Right ? Directions.Up : player.Direction - 1
            },
            _ => throw new System.Diagnostics.UnreachableException(),
        };
    }

    Player ExecuteMove(Order order, TileType[,] map, Player player)
    {
        var position = player.Position;
        var direction = player.Direction switch
        {
            Directions.Right => (1, 0),
            Directions.Down => (0, 1),
            Directions.Left => (-1, 0),
            Directions.Up => (0, -1),
            _ => throw new System.Diagnostics.UnreachableException(),
        };
        for (var i = 0; i < order.Move; i++)
        {
            position = NextPosition(map, position, direction);
        }
        return player with { Position = position };
    }

    private bool OutOfBounds(TileType[,] map, int x, int y)
    {
        return x < 0 || x >= map.GetLength(0) || y < 0 || y >= map.GetLength(1);
    }

    private (int x, int y) NextPosition(TileType[,] map, (int x, int y) pos, (int dx, int dy) dir)
    {
        var (nx, ny) = (pos.x + dir.dx, pos.y + dir.dy);
        if (OutOfBounds(map, nx, ny))
            return Teleport(map, pos, dir);
        return map[nx, ny] switch
        {
            TileType.Empty => Teleport(map, pos, dir),
            TileType.Open => (nx, ny),
            TileType.Solid => pos,
            _ => throw new System.Diagnostics.UnreachableException(),
        };
    }

    private (int x, int y) Teleport(TileType[,] map, (int x, int y) pos, (int dx, int dy) dir)
    {
        var newPosition = pos;
        while (!OutOfBounds(map, newPosition.x, newPosition.y) && map[newPosition.x, newPosition.y] != TileType.Empty)
        {
            newPosition.x -= dir.dx;
            newPosition.y -= dir.dy;
        }
        newPosition.x += dir.dx;
        newPosition.y += dir.dy;
        if (map[newPosition.x, newPosition.y] == TileType.Solid)
            return pos;
        else
            return newPosition;
    }

    public int Password(Player player)
    {
        return 1000 * (player.Position.y + 1) + 4 * (player.Position.x + 1) + (int)player.Direction;
    }
}

class Puzzle2 : IPuzzle
{
    public Cube Cube { get; private set; }
    int StartX;
    string Face;
    public (int X, int Y)[] DirDeltas { get; private set; } = new (int X, int Y)[]
    {
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    };

    public Puzzle2(string[] lines)
    {
        while (lines[0][StartX] != '.') StartX++;
        Cube = new Cube(lines, DirDeltas);
        Face = "front";
    }

    public Player Execute(Order order, Player player)
    {
        var (rotate, steps) = order;
        var position = player.Position;
        var directionIndex = (int)player.Direction;

        for (var i = 0; i < steps; i++)
        {
            var direction = DirDeltas[directionIndex];
            var newPosition = (X: position.x + direction.X, Y: position.y + direction.Y);
            var newDirectionIndex = directionIndex;
            var newFace = Face;
            if (!Cube.Segments[Cube.FaceSegment[Face]].TryGetValue(newPosition, out var valid))
            {
                newFace = Cube.FaceNeighbours[Face][(4 + directionIndex - Cube.FaceOffset[Face]) % 4];
                newPosition = position;
                var relativeFrom = (directionIndex + 2) % 4;
                var positionOffset = (4 + Array.IndexOf(Cube.FaceNeighbours[newFace], Face) - relativeFrom) % 4;
                var offset = Cube.FaceOffset[newFace];
                var rotations = (positionOffset + offset) % 4;

                for (var j = 0; j < rotations; j++)
                {
                    newDirectionIndex += 1;
                    newDirectionIndex %= 4;
                    newPosition = (Cube.Length - 1 - newPosition.Y, newPosition.X);
                }

                newPosition = newDirectionIndex switch
                {
                    0 => (0, newPosition.Y),
                    1 => (newPosition.X, 0),
                    2 => (Cube.Length - 1, newPosition.Y),
                    3 => (newPosition.X, Cube.Length - 1),
                    _ => throw new Exception()
                };

                valid = Cube.Segments[Cube.FaceSegment[newFace]][newPosition];
            }

            if (!valid) break;

            position = newPosition;
            Face = newFace;
            directionIndex = newDirectionIndex;
        }

        return ExecuteTurn(order, new Player((Directions)directionIndex, position));
    }

    public int Password(Player player)
    {
        var (xSegment, ySegment) = Cube.FaceSegment[Face];
        var column = xSegment * Cube.Length + player.Position.x + 1;
        var row = ySegment * Cube.Length + player.Position.y + 1;

        return 1000 * row + 4 * column + (int)player.Direction;
    }

    Player ExecuteTurn(Order order, Player player)
    {
        return order.Rotation switch
        {
            Rotations.None => player,
            Rotations.Clockwise => player with
            {
                Direction = player.Direction == Directions.Up ? Directions.Right : player.Direction + 1
            },
            Rotations.Counterclockwise => player with
            {
                Direction = player.Direction == Directions.Right ? Directions.Up : player.Direction - 1
            },
            _ => throw new System.Diagnostics.UnreachableException(),
        };
    }
}

class Cube
{
    public Dictionary<string, string[]> FaceNeighbours { get; private set; }
    public int Length { get; private set; }
    public Dictionary<string, int> FaceOffset { get; private set; } = new();
    public Dictionary<string, (int X, int Y)> FaceSegment = new();
    public Dictionary<(int X, int Y), Dictionary<(int X, int Y), bool>> Segments = new();

    public Cube(string[] lines, (int X, int Y)[] directions, int length = 50)
    {
        Length = length;
        FaceNeighbours = new Dictionary<string, string[]>
        {
            {"front", new [] { "right", "bottom", "left", "top"}},
            {"back", new [] { "left", "bottom", "right", "top"}},
            {"left", new [] { "front", "bottom", "back", "top"}},
            {"right", new [] { "back", "bottom", "front", "top"}},
            {"top", new [] { "right", "front", "left", "back"}},
            {"bottom", new [] { "right", "back", "left", "front"}}
        };

        for (var j = 0; j < lines.Length / length; j++)
        {
            var jFactor = j * length;
            for (var i = 0; i < lines[jFactor].Length / length; i++)
            {
                var iFactor = i * length;
                var segment = (i, j);
                Segments[segment] = new Dictionary<(int X, int Y), bool>();
                for (var y = 0; y < length; y++)
                {
                    var line = lines[jFactor + y];
                    for (var x = 0; x < length; x++)
                    {
                        var character = line[iFactor + x];
                        if (char.IsWhiteSpace(character))
                        {
                            continue;
                        }
                        var point = (X: x, Y: y);
                        if (character == '#')
                        {
                            Segments[segment][point] = false;
                        }
                        else if (character == '.')
                        {
                            Segments[segment][point] = true;
                        }
                    }
                }
            }
        }

        Segments = Segments.Where(s => s.Value.Any()).ToDictionary(s => s.Key, s => s.Value);

        var queue = new Queue<((int X, int Y) Segment, string Face, int FromDirection, string FromFace)>();
        var visited = new HashSet<(int X, int Y)>();
        visited.Add(Segments.Keys.First());
        queue.Enqueue((visited.First(), "front", 1, "top"));

        while (queue.Any())
        {
            var current = queue.Dequeue();
            FaceSegment[current.Face] = current.Segment;
            var relativeFrom = current.FromDirection + 2 % 4;
            var offset = (4 + relativeFrom - Array.IndexOf(FaceNeighbours[current.Face], current.FromFace)) % 4;
            FaceOffset[current.Face] = offset;

            for (var i = 0; i < 4; i++)
            {
                var direction = directions[i];
                var segment = (current.Segment.X + direction.X, current.Segment.Y + direction.Y);
                if (Segments.ContainsKey(segment) && !visited.Contains(segment))
                {
                    visited.Add(segment);
                    queue.Enqueue((segment, FaceNeighbours[current.Face][(4 + i - offset) % 4], i, current.Face));
                }
            }
        }
    }
}