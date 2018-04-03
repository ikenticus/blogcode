package loader

import (
	"fmt"
)

func Run(quote string) {
	fmt.Println("Given:", quote)
	Upper(quote)
	Lower(quote)
}
