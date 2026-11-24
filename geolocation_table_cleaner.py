import pandas as pd

from config.log_config import get_logger
from config.config import config
from .base_cleaner import BaseDataCleaner, data_type_mapping

logger = get_logger(__name__)


class GeolocationCleaner(BaseDataCleaner):
    """Geolocation-specific cleaning logic."""

    def __init__(self, raw_data: pd.DataFrame, table_name: str = config["GEOLOCATION_TABLE"]):
        super().__init__(raw_data, table_name)

    def clean(self) -> pd.DataFrame:
        """Main cleaning pipeline for geolocation table."""
        logger.info("Starting geolocation cleaning process")

        try:
            self.cleaned_data = self.raw_data.copy()
            self.cleaned_data.drop_duplicates(inplace=True)

            #create a single line for each zip code, keep mean of lat and long
            self.cleaned_data = self.cleaned_data.groupby('geolocation_zip_code_prefix', as_index=False).agg({
                'geolocation_lat': 'mean',
                'geolocation_lng': 'mean',
                'geolocation_city': 'first',
                'geolocation_state': 'first'
            })

            (self
                .data_type_validation(data_type_mapping.get(self.table_name)))

            logger.info("Geolocation cleaning process completed")
            return self.cleaned_data

        except Exception as e:
            logger.error(f"Error during geolocation cleaning: {str(e)}")
            raise


if __name__ == '__main__':
    # Example usage
    sample_data = pd.DataFrame({
        'geolocation_zip_code_prefix': [11, 11, 22],
        'geolocation_lat': [1, 2, 3],
        'geolocation_lng': [4, 5, 6],
        'geolocation_city': ['CityA', 'CityA', 'CityB'],
        'geolocation_state': ['StateA', 'StateA', 'StateB']
    })

    cleaner = GeolocationCleaner(sample_data)
    cleaned_data = cleaner.clean()
    print(cleaned_data)