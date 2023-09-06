import sp500_data_collection
import sp500_data_compilation
import sp500_data_ml
import sp500_data_visualization

def main():
    sp500_data_collection.get_data_from_yahoo()
    sp500_data_compilation.compile_data()
    sp500_data_ml.do_ml()
    sp500_data_visualization.visualize_data()

if __name__ == "__main__":
    main()
