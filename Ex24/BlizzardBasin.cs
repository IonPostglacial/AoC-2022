using System.Collections;

record Blizzard(int x, int y, int dx, int dy)
{
    public int X { get; set; } = x;
    public int Y { get; set; } = y;
    public int Dx { get; set; } = dx;
    public int Dy { get; set; } = dy;
}

record struct Step(int X, int Y, int T)
{
    public int Heuristic(Step other)
    {
        return Math.Abs(X - other.X) + Math.Abs(Y - other.Y) + Math.Abs(T - other.T);
    }

    public int Heuristic2D((int x, int y) other)
    {
        return Math.Abs(X - other.x) + Math.Abs(Y - other.y);
    }
}

record Node(Step Step, int Heuristic, Node? Previous = null) : IComparable<Node>
{
    public int CompareTo(Node? node)
    {
        if (node == null) return -1;
        return Score.CompareTo(node.Score);
    }

    public int Score
    {
        get
        {
            return Step.T + Heuristic;
        }
    }
}

class PathFinder
{
    private static List<Step> reconstructPath(Step start, Node goal)
    {
        var path = new List<Step>();
        var currentNode = goal;

        while (currentNode != null && currentNode.Step != start)
        {
            if (currentNode != null)
            {
                path.Add(currentNode.Step);
                currentNode = currentNode.Previous;
            }
            else
            {
                return new List<Step>();
            }
        }
        path.Add(start);
        return path;
    }

    public static List<Step> PathBetween(BlizzardBasin grid, Step start, (int x, int y) goal)
    {
        var closedList = new Dictionary<Step, Node>();
        var openList = new PriorityQueue<Node, int>();
        var h = start.Heuristic(new Step(goal.x, goal.y, start.Heuristic2D(goal)));
        Span<Step> neighbors = stackalloc Step[grid.NeighborsMaxCount()];

        openList.Enqueue(new Node(start, h), h);

        while (openList.Count > 0)
        {
            var node = openList.Dequeue();

            if (node.Step.X == goal.x && node.Step.Y == goal.y)
            {
                return reconstructPath(start, node);
            }
            for (int i = 0; i < grid.WriteNeighbors(neighbors, node.Step); i++)
            {
                var neighbor = neighbors[i];
                var heuristic = neighbor.Heuristic(new Step(goal.x, goal.y, neighbor.T + neighbor.Heuristic2D(goal)));
                var newNode = new Node(neighbor, heuristic, node);
                if (!closedList.TryGetValue(neighbor, out var oldNode) || newNode.Score < oldNode.Score)
                {
                    closedList[neighbor] = newNode;
                    openList.Enqueue(newNode, newNode.Score);
                }
            }
        }
        return new List<Step>();
    }
}

class BlizzardBasin
{
    int Width { get; init; }
    int Height { get; init; }
    List<BitArray> HorizontalBlizMaps { get; init; }
    List<BitArray> VerticalBlizMaps { get; init; }

    BlizzardBasin(int w, int h, List<BitArray> hBlizzards, List<BitArray> vBlizzards)
    {
        Width = w;
        Height = h;
        HorizontalBlizMaps = hBlizzards;
        VerticalBlizMaps = vBlizzards;
    }

    static List<BitArray> SimulateBlizzards(List<Blizzard> blizzards, int width, int height, int cellsNum, int n)
    {
        var blizzardMaps = new List<BitArray>();
        for (var i = 0; i < n; i++)
        {
            var obstacles = new BitArray(cellsNum);
            foreach (var bliz in blizzards)
            {
                bliz.X += bliz.Dx;
                bliz.Y += bliz.Dy;
                if (bliz.X < 0) bliz.X += width;
                if (bliz.X >= width) bliz.X -= width;
                if (bliz.Y < 0) bliz.Y += height;
                if (bliz.Y >= height) bliz.Y -= height;
                obstacles[bliz.X + width * bliz.Y] = true;
            }
            blizzardMaps.Add(obstacles);
        }
        return blizzardMaps;
    }

    static BlizzardBasin ParseInput(string[] lines)
    {
        var height = lines.Length - 2;
        var width = lines[0].Length - 2;
        var cellsNum = width * height;
        var hBliz = new List<Blizzard>();
        var vBliz = new List<Blizzard>();
        for (var y = 1; y <= height; y++)
        {
            for (var x = 1; x <= width; x++)
            {
                var c = lines[y][x];
                switch (c)
                {
                    case '<':
                        hBliz.Add(new(x - 1, y - 1, -1, 0));
                        break;
                    case '>':
                        hBliz.Add(new(x - 1, y - 1, 1, 0));
                        break;
                    case '^':
                        vBliz.Add(new(x - 1, y - 1, 0, -1));
                        break;
                    case 'v':
                        vBliz.Add(new(x - 1, y - 1, 0, 1));
                        break;
                }
            }
        }
        var hBlizzards = SimulateBlizzards(hBliz, width, height, cellsNum, width);
        var vBlizzards = SimulateBlizzards(vBliz, width, height, cellsNum, height);
        return new BlizzardBasin(width, height, hBlizzards, vBlizzards);
    }

    bool IsObstacle(Step pos)
    {
        var id = pos.X + Width * pos.Y;
        if (pos.X == 0 && pos.Y == -1 || pos.X == Width-1 && pos.Y == Height)
            return false;
        if (pos.X < 0 || pos.Y < 0 || pos.X >= Width || pos.Y >= Height)
            return true;
        return HorizontalBlizMaps[pos.T % Width][id] || VerticalBlizMaps[pos.T % Height][id];
    }

    internal int NeighborsMaxCount() => 5;

    internal int WriteNeighbors(Span<Step> neighbors, Step step)
    {
        var neighboursCount = 0;
        var left = new Step(step.X - 1, step.Y, step.T + 1);
        var top = new Step(step.X, step.Y - 1, step.T + 1);
        var right = new Step(step.X + 1, step.Y, step.T + 1);
        var bottom = new Step(step.X, step.Y + 1, step.T + 1);
        var wait = new Step(step.X, step.Y, step.T + 1);

        if (!IsObstacle(left))
            neighbors[neighboursCount++] = left;
        if (!IsObstacle(top))
            neighbors[neighboursCount++] = top;
        if (!IsObstacle(right))
            neighbors[neighboursCount++] = right;
        if (!IsObstacle(bottom))
            neighbors[neighboursCount++] = bottom;
        if (!IsObstacle(wait))
            neighbors[neighboursCount++] = wait;
        return neighboursCount;
    }

    public static void Main(string[] args)
    {
        var lines = System.IO.File.ReadAllLines("input.txt");
        var basin = ParseInput(lines);
        if (args.Length == 0)
        {
            Console.WriteLine("part 1 or part 2 ?");
            return;
        }
        if (args[0] == "1")
        {
            var path = PathFinder.PathBetween(basin, new (0, -1, 0), (basin.Width-1, basin.Height));
            Console.WriteLine(path[0].T + 1);
        }
        if (args[0] == "2") 
        {
            var path = PathFinder.PathBetween(basin, new (0, -1, 0), (basin.Width-1, basin.Height));
            var back = PathFinder.PathBetween(basin, path[0], (0, -1));
            var backAgain = PathFinder.PathBetween(basin, back[0], (basin.Width-1, basin.Height));
            Console.WriteLine(backAgain[0].T + 1);
        }
    }
}

