from deep_translator import GoogleTranslator
from langdetect import detect
from product.models import Product
from optimum.pipelines import pipeline


class CategoryPredictor:
    def __init__(self):
        self.category_classifier = pipeline("zero-shot-classification", accelerator="ort")

    def _translate_text(self, text):
        language = detect(text)
        if language == "en":
            return text

        return GoogleTranslator(source='auto', target='en').translate(text)

    def predict(self, product_name):
        product_name_translated = self._translate_text(product_name)
        candidate_labels = [c[0] for c in Product.ProductCategoryChoices]
        return self.category_classifier(product_name_translated, candidate_labels=candidate_labels)["labels"][0]
