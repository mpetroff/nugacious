from django.shortcuts import render
import quantity
import pint

comparator = quantity.comparator()

def home(request):
    '''
    Home page
    '''
    return render(request, 'home.html')

def about(request):
    '''
    About page
    '''
    return render(request, 'about.html')

def comparison(request):
    '''
    Comparison results
    '''
    query = request.GET.get('i')
    
    if query == '':
        return render(request, 'error.html', {
            'query': query,
            'empty_error': 'yes'
        })
    
    try:
        input_interp, closest_match, close_matches, random_matches \
            = comparator.compare(query)
    except quantity.UnsupportedDimensionsError as e:
        return render(request, 'error.html', {
            'query': query,
            'dimension_error': str(e)
        })
    except quantity.NoDimensionsError:
        return render(request, 'error.html', {
            'query': query,
            'no_dimensions_error': 'yes'
        })
    except pint.UndefinedUnitError as e:
        unit = e.unit_names.pop()
        return render(request, 'error.html', {
            'query': query,
            'unit_error': unit
        })
    except Exception:
        return render(request, 'error.html', {
            'query': query
        })
    closest_match_html = closest_match.natural_language()
    close_matches_html = []
    for m in close_matches:
        close_matches_html.append(m.natural_language())
    random_matches_html = []
    for m in random_matches:
        random_matches_html.append(m.natural_language())
    return render(request, 'comparison.html', {
        'input': input_interp,
        'closest_match': closest_match_html,
        'close_matches': close_matches_html,
        'random_matches': random_matches_html,
        'query': query
    })
