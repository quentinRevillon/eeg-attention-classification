(function() {
            var sort_by = "{{ sort_by }}";
            var sort_order = "{{ sort_order }}";
            var links = document.querySelectorAll('th.sortable a');
            for (var i = 0; i < links.length; i++) {
                if (links[i].href.indexOf(sort_by) != -1) {
                    links[i].classList.add(sort_order);
                }
            }
        })();