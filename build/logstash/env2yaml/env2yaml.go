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
	if len(os.Args) != 2 {
		log.Fatalf("usage: env2yaml FILENAME")
	}
	settingsFilePath := os.Args[1]

	settingsFile, err := ioutil.ReadFile(settingsFilePath)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	// Read the original settings file into a map.
	settings := make(map[string]interface{})
	err = yaml.Unmarshal(settingsFile, &settings)
	if err != nil {
		log.Fatalf("error: %v", err)
	}

	// Merge any settings found in the environment.
	for _, line := range os.Environ() {
		kv := strings.Split(line, "=")
		key := kv[0]
		value := kv[1]
		if strings.ContainsRune(key, '.') {
			log.Printf("Setting from environment '%s: %s'", key, value)
			settings[key] = TypifyString(value)
		}
	}

	output, err := yaml.Marshal(&settings)
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
