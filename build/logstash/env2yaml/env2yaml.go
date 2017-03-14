// env2yaml
//
// Merge environment variables into logstash.yml.
// For example, running Docker with:
//
//   docker run -e pipeline.workers=6
//
// will cause logstash.yml to contain the line:
//
//   pipeline.workers: 6
//
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

// If the given string can be converted to a boolan then do so, returning
// the resulting bool. Otherwise, return the string unmodified.
func StringToBoolIfPossible(str string) interface{} {
	if str == "false" {
		return false
	} else if str == "true" {
		return true
	} else {
		return str
	}
}

// Try to cast string representations of int, bool to actual
// int and bool types. This will help with YAML serialization.
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
