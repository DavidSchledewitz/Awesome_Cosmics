void histo_axis()
{
  // don't set the axis title here, but below, directly on the axis
  TH1F *histo = new TH1F("histo","A histogram",10,0,10);
  histo->Fill(4,2);
  histo->Fill(5,6);
  histo->Fill(6,4);

  // The histogram axis are own classes (TAxis), the can be accessed
  // using GetXaxis(), GetYaxix(), GetZaxis()
  TAxis *xaxis=histo->GetXaxis();
  TAxis *yaxis=histo->GetYaxis();

  // for example change the title
  xaxis->SetTitle("value");
  yaxis->SetTitle("entries");
  // for example change the size and offset of the title
  yaxis->SetTitleSize(0.08);
  yaxis->SetTitleOffset(0.55);
  // for example change the label size
  yaxis->SetLabelSize(0.06);
  
  // Draw a clone freezing the current state of the histo
  histo->DrawClone("HIST");
  
  // Create a new canvas (see later today) and draw the histogram with modified axis ranges
  TCanvas* c = new TCanvas();
  
  
  // Set the range of the axis from 3 to 8 (value on the axis) via SetRangeUser
  xaxis->SetRangeUser(3, 8);
  
  // Alternatively, one can use SetRange to set the range using the bin indices instead:
  //xaxis->SetRange(4, 8);
  histo->Draw("HIST");
  
  // NOTE: Have you noticed the subtlety? The mean of the histogram changes, if you set a range, although the new range
  // includes all bins with non-zero content. Reason: each time the histogram is filled, the mean is calculated automatically
  // using the REAL point where the histogram is filled. Once the range is changed, the mean is re-calculated, but in that case,
  // the REAL position is not known anymore. Instead, the centre of the bin is used. Exampel: histogram with bin from 1 to 2.
  // If you call histo->Fill(1.1), the "real" mean is 1.1. If you set a range, then the histogram "sees" one entry in the bin
  // with centre 1.5, so the "new mean" is then calculated to be 1.5.
}




