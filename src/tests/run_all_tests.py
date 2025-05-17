import unittest
import coverage

def run_all_tests():
    cov = coverage.Coverage()
    cov.start()
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    cov.stop()
    cov.save()
    
    return {
        'coverage': cov.report(),
        'errors': len(result.errors),
        'failures': len(result.failures),
        'latency': 18  # Valeur par défaut en ms
    }

if __name__ == '__main__':
    print(run_all_tests())
