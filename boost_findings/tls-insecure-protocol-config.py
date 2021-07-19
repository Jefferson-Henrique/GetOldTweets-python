package main

import (
    "crypto/tls"
    "fmt"
    "io/ioutil"
    "net/http"
)

func main() {
    client := &http.Client{
        Transport: &http.Transport{
            TLSClientConfig: &tls.Config{
                // The following version are insecure: VersionTLS10, VersionTLS11, VersionSSL30
                MinVersion: tls.VersionSSL30, // Allow insecure version the TCP protocol (SSLv3)
                // Allowing cipher suites with broken cryptography is risky
                CipherSuites: []uint16{
                    tls.TLS_RSA_WITH_RC4_128_SHA,
                    tls.TLS_RSA_WITH_AES_128_CBC_SHA256,
                },
            },
        },
    }

    fetch(client, "https://tls-v1-0.badssl.com:1010/")
    fetch(client, "https://rc4.badssl.com/")
}

func fetch(client *http.Client, url string) {
    resp, err := client.Get(url)
    if err != nil {
        fmt.Println(err)
    } else {
        defer resp.Body.Close()
        body, _ := ioutil.ReadAll(resp.Body)
        fmt.Println(">>> Data received over insecure TLS connection (broken cryptography)")
        fmt.Println(string(body))
    }
}
