// env2yaml
//
// Merge environment variables into logstash.yml.
// For example, running Docker with:
//
//   docker run -e pipeline.workers=6
//
// or
//
//   docker run -e PIPELINE_WORKERS=6
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

// If the given string can be converted to a boolean then do so, returning
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

func normalizeSetting(setting string) string {
	downcased := strings.ToLower(setting)
	dotted := strings.Replace(downcased, "_", ".", -1)
	return dotted
}

func isValidSetting(setting string) bool {
	valid_settings := []string {
		"node.name",
		"path.data",
		"pipeline.workers",
		"pipeline.output.workers",
		"pipeline.batch.size",
		"pipeline.batch.delay",
		"pipeline.unsafe_shutdown",
		"path.config",
		"config.string",
		"config.test_and_exit",
		"config.reload.automatic",
		"config.reload.interval",
		"config.debug",
		"queue.type",
		"path.queue",
		"queue.page_capacity",
		"queue.max_events",
		"queue.max_bytes",
		"queue.checkpoint.acks",
		"queue.checkpoint.writes",
		"queue.checkpoint.interval",
		"http.host",
		"http.port",
		"log.level",
		"log.format",
		"path.logs",
		"path.plugins",
		"xpack.monitoring.enabled",
		"xpack.monitoring.collection.interval",
		"xpack.monitoring.elasticsearch.url",
		"xpack.monitoring.elasticsearch.username",
		"xpack.monitoring.elasticsearch.password",
		"xpack.monitoring.elasticsearch.ssl.ca",
		"xpack.monitoring.elasticsearch.ssl.truststore.path",
		"xpack.monitoring.elasticsearch.ssl.truststore.password",
	}

	for _, valid_setting := range valid_settings {
		if normalizeSetting(setting) == valid_setting {
			return true
		}
	}
	return false
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

	// Merge any valid settings found in the environment.
	foundNewSettings := false
	for _, line := range os.Environ() {
		kv := strings.Split(line, "=")
		key := kv[0]
		value := kv[1]
		if isValidSetting(key) {
			foundNewSettings = true
			setting := normalizeSetting(key)
			log.Printf("Setting from environment '%s: %s'", setting, value)
			settings[setting] = TypifyString(value)
		}
	}

	if foundNewSettings {
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
}
