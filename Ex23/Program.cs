using System.Collections.Generic;

World ParseInput(string[] lines)
{
    var height = lines.Length;
    var width = lines[0].Length;
    var elves = new HashSet<(int x, int y)>();
    for (var y = 0; y < height; y++)
    {
        for (var x = 0; x < width; x++)
        {
            if (lines[y][x] == '#')
            {
                elves.Add((x, y));
            }
            
        }
    }
    return new World(elves);
}

var lines = System.IO.File.ReadAllLines("input.txt");
var world = ParseInput(lines);
if (args.Length < 1)
{
    Console.WriteLine("part 1 or 2 ?");
    return;
}
if (args[0] == "1")
{
    for (var i = 0; i < 10; i++)
    {
        world.Round();
    }
    Console.WriteLine(world.EmptyArea());
}

if (args[0] == "2")
{
    var round = 1;
    while (world.Round())
    {
        round++;
    }
    Console.WriteLine(round);
}

record World(HashSet<(int x, int y)> Elves) {
    static readonly (int, int)[] Deltas = {
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
    };
    const UInt32 NorthMask = 0b00000000_00000000_00000000_00000111;
    const UInt32 SouthMask = 0b00000000_00000000_00000000_11100000;
    const UInt32 WestMask = 0b00000000_00000000_00000000_00101001;
    const UInt32 EastMask = 0b00000000_00000000_00000000_10010100;
    static readonly UInt32[] DirMasks = new UInt32[]{ NorthMask, SouthMask, WestMask, EastMask };
    static readonly (int, int)[] DirDeltas = { (0, -1), (0, 1), (-1, 0), (1, 0) };

    int firstDir = 0;
    Dictionary<(int x, int y), List<(int x, int y)>> ProposedMoves = new();

    void AddProposedMove((int, int) dest, (int, int) src)
    {
        if (ProposedMoves.TryGetValue(dest, out var list))
            list.Add(src);
        else
            ProposedMoves.Add(dest, new List<(int, int)>{src});
    }

    public bool Round()
    {
        ProposedMoves.Clear();
        foreach(var (x, y) in Elves)
        {
            UInt32 neighbors = 0;
            for(int i = 0; i < Deltas.Length; i++)
            {
                var (dx, dy) = Deltas[i];
                var pos = (x + dx, y + dy);
                if (Elves.Contains(pos))
                    neighbors |= (1u << i);
            }
            if (neighbors == 0) continue;
            for (var i = 0; i < DirDeltas.Length; i++)
            {
                var n = (firstDir + i) % DirDeltas.Length;
                var mask = DirMasks[n];
                var (dx, dy) = DirDeltas[n];
                if ((neighbors & mask) == 0)
                {
                    AddProposedMove((x + dx, y + dy), (x, y));
                    break;
                }
            }
        }
        foreach (var (dest, sources) in ProposedMoves)
        {
            if (sources.Count == 1)
            {
                Elves.Remove(sources[0]);
                Elves.Add(dest);
            }
        }
        firstDir++;
        return ProposedMoves.Count > 0;
    }

    public (int left, int right, int top, int bottom) Bounds()
    {
        int left = int.MaxValue, right = int.MinValue, top = int.MaxValue, bottom = int.MinValue;
        foreach(var (x, y) in Elves)
        {
            left = Math.Min(left, x);
            right = Math.Max(right, x);
            top = Math.Min(top, y);
            bottom = Math.Max(bottom, y);
        }
        return (left, right, top, bottom);
    }

    int Area()
    {
        var (left, right, top, bottom) = Bounds();
        return (1 + right - left) * (1 + bottom - top);
    }

    public void Display()
    {
        var (left, right, top, bottom) = Bounds();
        for (var y = top; y <= bottom; y++) {
            for (var x = left; x <= right; x++)
            {
                Console.Write(Elves.Contains((x, y)) ? "#" : ".");
            }
            Console.WriteLine();
        }
    }

    public int EmptyArea()
    {
        return Area() - Elves.Count;
    }
}