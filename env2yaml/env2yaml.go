package main

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

// If the given string can be converted to an integer then do so, returning
// the resulting integer. Otherwise, return the string unmodified.
func StringToIntIfPossible(str string) interface{} {
	intValue, err := strconv.Atoi(str)
	if err == nil {
		return intValue
	} else {
		return str
	}
}

func StringToBoolIfPossible(str string) interface{} {
	if str == "false" {
		return false
	} else if str == "true" {
		return true
	} else {
		return str
	}
}

func TypifyString(str string) interface{} {
	var typified interface{}
	typified = StringToIntIfPossible(str)
	if str == typified {
		// It wasn't an int. Try bool instead.
		typified = StringToBoolIfPossible(str)
	}
	return typified
}

func main() {
	settingsFilePath := os.Args[1]
	conf := make(map[string]interface{})

	conf_file, err := ioutil.ReadFile(settingsFilePath)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	err = yaml.Unmarshal(conf_file, &conf)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	for _, line := range os.Environ() {
		key_and_value := strings.Split(line, "=")
		key := key_and_value[0]
		if strings.ContainsRune(key, '.') {
			value := key_and_value[1]
			log.Printf("Setting from environment '%s: %s'", key, value)
			conf[key] = TypifyString(value)
		}
	}

	output, err := yaml.Marshal(&conf)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	stat, err := os.Stat(settingsFilePath)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	err = ioutil.WriteFile(settingsFilePath, output, stat.Mode())
	if err != nil {
		log.Fatalf("error: %v", err)
	}
}
