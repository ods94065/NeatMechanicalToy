import chai
from chai import comparators
import json
from rest_framework import test


class ItemsAnyOrder(comparators.Comparator):
    """A comparator that matches two sequences that have the same items in any order.
    The items must be hashable, and the sequences must be convertible to sets via set()."""
    def __init__(self, expected_list):
        self.expected_set = set(expected_list)

    def test(self, actual_obj):
        try:
            return self.expected_set == set(actual_obj)
        except Exception:
            return False

    def __repr__(self):
        return 'ItemsAnyOrder(%s)' % repr(list(self.expected_set))


class TestCase(chai.Chai, test.APITestCase):
    def assertJsonEqual(self, json_struct_expectation, json_struct, strict=False):
        """Compares a JSON structure (dict, list, or primitive) against an expectation structure.
        Args:
            json_struct_expectation: dict, list, primitive, or comparator.  A structure that mimics
                the json_struct, but may use Chai comparators as keys or values.
            json_struct: dict, list, or primitive.  The parsed JSON value to match.
            strict: boolean.  If True, ensure exact match, otherwise ignore extra dict keys in the
                json_struct.
        """
        errors = self._assertJsonFragmentEqual(json_struct_expectation, json_struct, strict=strict)
        if errors:
            # Can't dump expected JSON here since it may have comparators as keys.
            self.fail('Mismatched %s\nActual: %s' %
                (errors.prettyPrint(), json.dumps(json_struct, indent=2)))

    def _assertJsonFragmentEqual(self, o1, o2, strict=False):
        if isinstance(o1, dict):
            if not isinstance(o2, dict):
                return _AtomMismatch('not a dict: %r' % (o2,))
            errors = _DictMismatch()
            if len(o1) == 1 and len(o2) == 1:
                key = o1.iterkeys().next()
                key2 = o2.iterkeys().next()
                if key == key2:
                    error = self._assertJsonFragmentEqual(o1[key], o2[key2], strict=strict)
                else:
                    error = _AtomMismatch(
                        'different keys in singleton dicts: %r != %r' % (key, key2))
                errors.add(key, error)
            else:
                used_keys = set()
                for key in o1:
                    if key not in o2:
                        for key2 in o2:
                            if key2 in used_keys: continue
                            var_cache = comparators.Variable._cache.copy()
                            error = self._assertJsonFragmentEqual(o1[key], o2[key2], strict=strict)
                            if not error and key == key2:
                                used_keys.add(key2)
                                errors.add(key, error)
                                break
                            else:
                                # Revert captured variables
                                comparators.Variable._cache.clear()
                                comparators.Variable._cache.update(var_cache)
                        else:
                            errors.add(key, _AtomMismatch('missing %r' % (o1[key],)))
                    else:
                        used_keys.add(key)
                        errors.add(
                            key, self._assertJsonFragmentEqual(o1[key], o2[key], strict=strict))
                if strict:
                    for key in o2:
                        if key not in o1:
                            errors.add(key, _AtomMismatch('extra %r' % (o2[key],)))
            return errors
        if isinstance(o1, list):
            if not isinstance(o2, list):
                return _AtomMismatch('not a list: %r' % (o2,))
            errors = _ListMismatch()
            for i in xrange(max(len(o1), len(o2))):
                if i >= len(o1):
                    errors.add(i, _AtomMismatch('extra %r' % (o2[i],)))
                elif i >= len(o2):
                    errors.add(i, _AtomMismatch('missing %r' % (o1[i],)))
                else:
                    errors.add(i, self._assertJsonFragmentEqual(o1[i], o2[i], strict=strict))
            return errors
        if not o1 == o2:  # don't use != because Chai comparators don't define it properly
            return _AtomMismatch('%r != %r' % (o1, o2))
        return None

    # convenience for accessing a comparator, following the pattern in ChaiBase
    items_any_order = ItemsAnyOrder


class _AtomMismatch(object):
    def __init__(self, error):
        self.error = error

    def __nonzero__(self):
        return True

    def prettyPrint(self, path='', indent=0):
        message = '  ' * indent
        if path:
            message += path + ': '
        message += self.error
        return message


class _DictMismatch(object):
    def __init__(self):
        self.errors = {}

    def __nonzero__(self):
        return bool(self.errors)

    def add(self, key, error):
        if error:
            self.errors[key] = error

    def prettyPrint(self, path='', indent=0):
        if not self.errors: return ''
        if len(self.errors) == 1:
            key, value = self.errors.iteritems().next()
            return value.prettyPrint(
                path=path + self._formatKey(key, bool(path)), indent=indent)
        message = self._prettyPrintFull(indent)
        if path:
            message = '%s: %s' % (path, message)
        return message

    def _formatKey(self, key, appending):
        return ('.' if appending else '') + str(key)

    def _prettyPrintFull(self, indent):
        return (
            '{\n' + '\n'.join(
                self.errors[key].prettyPrint(path=self._formatKey(key, False), indent=indent + 1)
                for key in sorted(self.errors.keys())
            ) + '\n' + '  ' * indent + '}')


class _ListMismatch(_DictMismatch):
    def _formatKey(self, key, unused_appending):
        return '[%s]' % key
