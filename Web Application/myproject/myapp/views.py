# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DateRangeForm
from .utils import process_data_range
import os
import csv
from io import StringIO  # Ensure this import is here


def index(request):
    error_message = None
    csv_path = None
    csv_data = None
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"].strftime("%d-%m-%Y")
            end_date = form.cleaned_data["end_date"].strftime("%d-%m-%Y")

            # Process data range
            df, error_message, csv_path = process_data_range(start_date, end_date)

            if df is not None:
                # Save to a string buffer
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                # Read CSV file for displaying in the template
                csv_buffer.seek(0)  # Reset buffer position to the start
                reader = csv.reader(csv_buffer)
                csv_data = list(reader)

                return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "csv_data": csv_data,
                        "message": f"Data from {start_date} to {end_date}",
                        "csv_path": os.path.basename(csv_path),
                    },
                )
    else:
        form = DateRangeForm()

    return render(request, "index.html", {"form": form, "error_message": error_message})


def download_csv(request, file_path):
    file_path = os.path.join("myapp/Data", file_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="text/csv")
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(file_path)}"'
            )
            return response
    else:
        return HttpResponse("File not found.", status=404)
