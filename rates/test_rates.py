from rate_calculator import calculate_visit_rates, format_rate_table

def test_visit_rates():
    """
    Test both ER and hospital visit rate calculations and display results.
    """
    print("\nTesting Visit Rate Calculations...")
    print("----------------------------------------")
    
    # Test ER visit rates
    print("\nER Visit Rates:")
    er_rates_df = calculate_visit_rates('er')
    print(format_rate_table(er_rates_df, 'er'))
    
    # Test hospital visit rates
    print("\nHospital Visit Rates:")
    hospital_rates_df = calculate_visit_rates('hospital')
    print(format_rate_table(hospital_rates_df, 'hospital'))
    
    # Basic validation for ER rates
    print("\nER Visit Rate Validation:")
    print(f"1. Number of years with data: {len(er_rates_df)}")
    print(f"2. Total member months: {er_rates_df['total_member_months'].sum():,.0f}")
    print(f"3. Total ER visits: {er_rates_df['visit_count'].sum():,.0f}")
    print(f"4. Average ER visit rate: {er_rates_df['rate_per_1000_member_months'].mean():.2f}")
    
    # Basic validation for hospital rates
    print("\nHospital Visit Rate Validation:")
    print(f"1. Number of years with data: {len(hospital_rates_df)}")
    print(f"2. Total member months: {hospital_rates_df['total_member_months'].sum():,.0f}")
    print(f"3. Total hospital visits: {hospital_rates_df['visit_count'].sum():,.0f}")
    print(f"4. Average hospital visit rate: {hospital_rates_df['rate_per_1000_member_months'].mean():.2f}")

if __name__ == "__main__":
    test_visit_rates() 