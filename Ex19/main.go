package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"sync"
)

type Resource int

const (
	Ore = Resource(iota)
	Clay
	Obsidian
	Geode
	NbResources = iota
	MaxDepth    = 32
)

var resourceNames = []string{"ore", "clay", "obsidian", "geode"}

func (res Resource) String() string {
	return resourceNames[res]
}

func ResourceFromString(s string) (Resource, error) {
	for i, name := range resourceNames {
		if s == name {
			return Resource(i), nil
		}
	}
	return Resource(0), fmt.Errorf("Unknown resource '%s'.", s)
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

type Blueprint struct {
	Num     int
	Costs   [NbResources][NbResources - 1]int
	MaxNeed [NbResources - 1]int
}

func parseInput(input io.Reader) []Blueprint {
	scanner := bufio.NewScanner(input)
	re := regexp.MustCompile(`Each (\w+) robot costs (\d+) (\w+)(?: and (\d+) (\w+))?.`)
	blueprints := make([]Blueprint, 0, 30)
	num := 0
	for scanner.Scan() {
		num++
		blueprint := Blueprint{Num: num}
		ms := re.FindAllStringSubmatch(scanner.Text(), -1)
		for _, m := range ms {
			robot, err := ResourceFromString(m[1])
			if err != nil {
				panic(err)
			}
			for j := 0; j < 2; j++ {
				resCost := m[2*j+2]
				resName := m[2*j+3]
				if resCost == "" {
					continue
				}
				cost, err := strconv.Atoi(resCost)
				if err != nil {
					panic(err)
				}
				res, err := ResourceFromString(resName)
				if err != nil {
					panic(err)
				}
				blueprint.Costs[robot][res] = cost
			}
		}
		blueprint.MaxNeed[Ore] =
			max(blueprint.Costs[Ore][Ore],
				max(blueprint.Costs[Clay][Ore],
					max(blueprint.Costs[Obsidian][Ore],
						blueprint.Costs[Geode][Ore])))
		blueprint.MaxNeed[Clay] = blueprint.Costs[Obsidian][Clay]
		blueprint.MaxNeed[Obsidian] = blueprint.Costs[Geode][Obsidian]
		blueprints = append(blueprints, blueprint)
	}
	return blueprints
}

type State struct {
	Remaining  int
	Resources  [NbResources]int
	Production [NbResources]int
}

func (state *State) NextState() *State {
	return &State{state.Remaining - 1, state.Resources, state.Production}
}

func (state *State) IsTimeout() bool {
	return state.Remaining <= 0
}

func (state *State) CanBuyRobot(bp *Blueprint, robot Resource) bool {
	for i, cost := range bp.Costs[robot] {
		if cost > state.Resources[i] {
			return false
		}
	}
	return true
}

func (state *State) NeedRobot(bp *Blueprint, robot Resource) bool {
	switch robot {
	case Obsidian:
		return state.Production[Clay] > 0 && state.Production[Obsidian] < bp.MaxNeed[Obsidian]
	case Geode:
		return state.Production[Obsidian] > 0
	default:
		return state.Production[robot] < bp.MaxNeed[robot]
	}
}

func (state *State) Buy(bp *Blueprint, robot Resource) {
	for i, cost := range bp.Costs[robot] {
		state.Resources[i] -= cost
	}
	state.Production[robot]++
}

func (state *State) MineResource() {
	for i, yield := range state.Production {
		state.Resources[i] += yield
	}
}

type Explorer struct {
	blueprint       *Blueprint
	visited         map[State]int
	bestByRemaining []int
	limits          []int
}

func NewExplorer(blueprint *Blueprint) *Explorer {
	limits := make([]int, MaxDepth+1)
	acc := 0
	for i := 0; i < len(limits); i++ {
		limits[i] = acc
		acc += i
	}
	return &Explorer{
		blueprint:       blueprint,
		visited:         make(map[State]int),
		bestByRemaining: make([]int, MaxDepth+1),
		limits:          limits,
	}
}

func (xp *Explorer) MemoReturn(state *State, maxGeodes int) int {
	xp.visited[*state] = maxGeodes
	best := xp.bestByRemaining[state.Remaining]
	if maxGeodes > best {
		xp.bestByRemaining[state.Remaining] = maxGeodes
	}
	return maxGeodes
}

func (xp *Explorer) MaxGeodes(state *State) int {
	if state.IsTimeout() {
		return xp.MemoReturn(state, state.Resources[Geode])
	}
	potentialGeodes := state.Resources[Geode] + state.Production[Geode]*state.Remaining + xp.limits[state.Remaining]
	if potentialGeodes < xp.bestByRemaining[state.Remaining] {
		return 0
	}
	if prevState, ok := xp.visited[*state]; ok {
		return prevState
	}
	noopState := state.NextState()
	noopState.MineResource()
	maxGeodes := xp.MaxGeodes(noopState)
	for robot := Ore; robot < NbResources; robot++ {
		if state.NeedRobot(xp.blueprint, robot) && state.CanBuyRobot(xp.blueprint, robot) {
			buyState := state.NextState()
			buyState.MineResource()
			buyState.Buy(xp.blueprint, robot)
			maxGeodes = max(maxGeodes, xp.MaxGeodes(buyState))
		}
	}
	return xp.MemoReturn(state, maxGeodes)
}

func main() {
	input, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	blueprints := parseInput(input)
	switch os.Args[1] {
	case "1":
		results := make([]int, len(blueprints))
		var wg sync.WaitGroup
		wg.Add(len(results))
		for i, blueprint := range blueprints {
			go func(i int, blueprint Blueprint) {
				xp := NewExplorer(&blueprint)
				res := xp.MaxGeodes(&State{24, [NbResources]int{}, [NbResources]int{Ore: 1}})
				results[i] = res * blueprint.Num
				wg.Done()
			}(i, blueprint)
		}
		wg.Wait()
		sum := 0
		for _, n := range results {
			sum += n
		}
		fmt.Println(sum)
	case "2":
		nbBlueprints := min(len(blueprints), 3)
		results := make([]int, nbBlueprints)
		var wg sync.WaitGroup
		wg.Add(nbBlueprints)
		for i, blueprint := range blueprints[:nbBlueprints] {
			go func(i int, blueprint Blueprint) {
				xp := NewExplorer(&blueprint)
				res := xp.MaxGeodes(&State{MaxDepth, [NbResources]int{}, [NbResources]int{Ore: 1}})
				results[i] = res
				wg.Done()
			}(i, blueprint)
		}
		wg.Wait()
		res := 1
		for _, n := range results {
			res *= n
		}
		fmt.Println(res)
	}
}
