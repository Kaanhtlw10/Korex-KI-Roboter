
			function zeige(id) {
				var seiten = document.getElementsByClassName("seite");
				for (var i = 0; i < seiten.length; i++) {
					seiten[i].classList.remove("aktiv");}
				document.getElementById(id).classList.add("aktiv");}
		
		