fun init() {
	var tab, i, j

	tab : maketable(10, 10, handler)
	i : 0
	loop {
		until .i > 9
		j : 0
		loop {
			until .j > 9
			setcell(.tab, .i, .j, "&#x25a2")
			if (.i + .j) % 2 == 1 {
				setcellcolor(.tab, .i, .j, "lightgreen")
			}
			else {
				setcellcolor(.tab, .i, .j, "lightblue")
			}
			j : .j + 1
		}
		i : .i + 1
	}
}

fun handler(r, c) {
	iprint(.r)
	sprint(" ")
	iprint(.c)
	sprint("\n")
}
