"""
Benchmark evaluation script using the benchmark dataset.

This script demonstrates how to use the benchmark dataset to test
prompt performance and validate LLM outputs systematically.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from src.evaluation.error_categorizer import ErrorCategorizer
from src.evaluation.validators import ResponseValidator


def load_benchmark_dataset(filepath):
    """Load the benchmark dataset from YAML file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def evaluate_test_case(test_case, response, dataset):
    """
    Evaluate a test case against a response.
    
    Args:
        test_case: Test case configuration
        response: LLM-generated response
        dataset: Full benchmark dataset with reference data
        
    Returns:
        Dictionary with evaluation results
    """
    results = {
        "test_id": test_case["id"],
        "category": test_case["category"],
        "passed": True,
        "errors": [],
        "warnings": [],
        "metrics": {}
    }
    
    # Initialize components
    categorizer = ErrorCategorizer()
    
    # Configure validator with test case requirements
    config = test_case.get("expected_quality", {})
    if config:
        validator = ResponseValidator(config=config)
    else:
        validator = ResponseValidator()
    
    # 1. Check for hallucinations
    hallucination_indicators = dataset.get("hallucination_indicators", [])
    for indicator in hallucination_indicators:
        if indicator.lower() in response.lower():
            results["errors"].append(f"Hallucination indicator found: '{indicator}'")
            results["passed"] = False
    
    # 2. Validate response
    validation_result = validator.validate_response(
        response,
        test_case["prompt"],
        test_case.get("expected_elements", [])
    )
    
    results["metrics"]["overall_score"] = validation_result.overall_score
    results["metrics"]["validation_status"] = validation_result.status.value
    
    for metric in validation_result.metrics:
        results["metrics"][metric.name.lower().replace(" ", "_")] = {
            "score": metric.score,
            "passed": metric.passed
        }
        
        if not metric.passed:
            results["errors"].append(f"{metric.name} failed: {metric.details}")
            results["passed"] = False
    
    # 3. Check against reference facts if applicable
    if test_case["category"] == "factual_qa":
        reference_facts = {}
        for category in dataset.get("reference_facts", {}).values():
            for fact in category:
                reference_facts[fact["key"]] = fact["value"]
        
        fact_errors = categorizer.check_factual_accuracy(response, reference_facts)
        if fact_errors:
            for error in fact_errors:
                results["errors"].append(f"Factual error: {error.description}")
                results["passed"] = False
    
    return results


def run_benchmark_tests(dataset_path, sample_responses):
    """
    Run benchmark tests with sample responses.
    
    Args:
        dataset_path: Path to benchmark dataset YAML
        sample_responses: Dictionary mapping test_id to response text
    """
    print("=" * 70)
    print("BENCHMARK EVALUATION")
    print("=" * 70)
    
    # Load dataset
    dataset = load_benchmark_dataset(dataset_path)
    test_cases = dataset.get("test_cases", [])
    
    print(f"\nLoaded {len(test_cases)} test cases")
    print(f"Testing {len(sample_responses)} responses\n")
    
    # Run tests
    results = []
    for test_case in test_cases:
        test_id = test_case["id"]
        
        if test_id not in sample_responses:
            print(f"⊘ {test_id}: No response provided")
            continue
        
        response = sample_responses[test_id]
        result = evaluate_test_case(test_case, response, dataset)
        results.append(result)
        
        # Print result
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        print(f"{status} {test_id} ({result['category']})")
        print(f"     Score: {result['metrics']['overall_score']:.2f}")
        
        if result["errors"]:
            print("     Errors:")
            for error in result["errors"][:3]:  # Show first 3 errors
                print(f"       - {error}")
        
        print()
    
    # Summary
    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed

    if results:
        passed_pct = passed / len(results) * 100
        failed_pct = failed / len(results) * 100
    else:
        passed_pct = 0.0
        failed_pct = 0.0
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed} ({passed_pct:.1f}%)")
    print(f"Failed: {failed} ({failed_pct:.1f}%)")
    
    if results:
        avg_score = sum(r["metrics"]["overall_score"] for r in results) / len(results)
        print(f"Average Score: {avg_score:.2f}")
    
    print()
    
    return results


def main():
    """Run benchmark tests with sample responses."""
    
    # Define sample responses for testing
    sample_responses = {
        "tc_001": "The capital of France is Paris, a major European city.",
        
        "tc_002": """
        Photosynthesis is the process by which plants convert sunlight into energy.
        During this process, plants absorb carbon dioxide from the air and water from 
        the soil. Using sunlight as energy, they convert these into glucose (a sugar) 
        and release oxygen as a byproduct. This process occurs primarily in the leaves 
        of plants, specifically in structures called chloroplasts.
        """,
        
        "tc_003": """
        This function calculates the factorial of a number using recursion.
        It has a base case: if n is less than or equal to 1, it returns 1.
        Otherwise, it recursively calls itself with n-1 and multiplies the result by n.
        For example, factorial(5) would compute 5 * 4 * 3 * 2 * 1 = 120.
        """,
        
        "tc_004": """
        Climate change refers to long-term shifts in global temperature and weather patterns.
        Rising temperatures are causing significant environmental impacts including melting ice caps,
        rising sea levels, and more extreme weather events. The primary cause is human activities
        that release greenhouse gases into the atmosphere.
        """,
        
        "tc_005": """
        Given the statements that all A are B and all B are C, we can use the transitive property
        of logical statements to conclude that all A are C. This is because if every A is included
        in B, and every B is included in C, then by transitivity, every A must also be included in C.
        """
    }
    
    # Path to benchmark dataset
    dataset_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "benchmark_dataset.yaml"
    )
    
    # Run tests
    results = run_benchmark_tests(dataset_path, sample_responses)
    
    # Analyze results by category
    print("=" * 70)
    print("RESULTS BY CATEGORY")
    print("=" * 70)
    
    categories = {}
    for result in results:
        category = result["category"]
        if category not in categories:
            categories[category] = {"passed": 0, "total": 0, "scores": []}
        
        categories[category]["total"] += 1
        if result["passed"]:
            categories[category]["passed"] += 1
        categories[category]["scores"].append(result["metrics"]["overall_score"])
    
    for category, stats in categories.items():
        avg_score = sum(stats["scores"]) / len(stats["scores"])
        pass_rate = stats["passed"] / stats["total"] * 100
        print(f"\n{category}:")
        print(f"  Tests: {stats['total']}")
        print(f"  Pass Rate: {pass_rate:.1f}%")
        print(f"  Average Score: {avg_score:.2f}")
    
    print("\n" + "=" * 70)
    print("BENCHMARK EVALUATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
