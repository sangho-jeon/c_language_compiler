int func(int a, int b) {
	if (a >= 5) {
		a = 5.54;
	}
	else if (b <= 7) {
		b = 7;
	}

	else a = -6;

	for (int i = 0; i <= 3; i++) {
		a = a - b;
	}

	if ((a >= -4) == true) {
		print("hello");
		return 5;
	}

	else {
		return 0;
	}
}